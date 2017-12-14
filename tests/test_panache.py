# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.panache import STYLE_, STYLEDEF_, STYLES_, PanacheStyle, PanacheStyles, panache_yaml_format_variables, \
    parse_cmdline, get_yaml_lines, get_input_yaml, determine_style, compile_command_line, \
    substitute_style_vars


class MyTestCase(unittest.TestCase):

    def setUp(self):

        logging.getLogger().setLevel(logging.ERROR)

        self.style_dir = tempfile.mkdtemp()

        # create a temporary styles definition file
        stylesdef_txt = """
{STYLEDEF_}:
    html:
        {METADATA_}:
            lang: de
        {COMMANDLINE_}:
            toc: true
    en_html:
        {METADATA_}:
            lang: en
""".format(**panache_yaml_format_variables)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="2", suffix=".yaml", dir=self.style_dir) as f:
            f.writelines(stylesdef_txt)
            self.stylesdef_1 = f.name

        # create a temporary styles definition file
        stylesdef_txt = """
{STYLEDEF_}:        
    html:
        {METADATA_}:
            lang: en
            foo: bar
        {COMMANDLINE_}:
            toc: true
    it_html:
        {PARENT_}: html
        {METADATA_}:
            lang: it
""".format(**panache_yaml_format_variables)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="1", suffix=".yaml", dir=self.style_dir) as f:
            f.writelines(stylesdef_txt)
            self.stylesdef_2 = f.name

        # create a temporary markdown file
        markdown = """
---
{STYLES_}:
    wiki: tsihtml
{STYLEDEF_}:        
    html:
        {METADATA_}:
            lang: ru 
    tsihtml:
        {COMMANDLINE_}:
            toc: false
---

# Header 1

## Header 2
""".format(**panache_yaml_format_variables)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(markdown)
            self.markdown = f.name

    def tearDown(self):
        os.remove(self.stylesdef_1)
        os.remove(self.stylesdef_2)
        os.remove(self.markdown)

    @staticmethod
    def construct_lines(txt):
        return list(map(lambda x: x + '\n', re.split(r'\n', txt)))

    def test_get_yaml_lines_1(self):
        lines = self.construct_lines("---\nfoo: bar\n---\nblub")
        result = get_yaml_lines(lines)
        expected = ['foo: bar\n']
        self.assertEqual(result, expected)

    def test_get_yaml_lines_2(self):
        lines = self.construct_lines("\n\n---\nfoo: bar\n---\n\nblub\n")
        result = get_yaml_lines(lines)
        expected = ['foo: bar\n']
        self.assertEqual(result, expected)

    def test_get_yaml_lines_3(self):
        lines = self.construct_lines("\n\n---\nfoo: bar\n...\n\nblub\n")
        result = get_yaml_lines(lines)
        expected = ['foo: bar\n']
        self.assertEqual(result, expected)

    def test_get_yaml_lines_4(self):
        lines = self.construct_lines("...\nfoo: bar\n...\nblub")
        result = get_yaml_lines(lines)
        expected = []
        self.assertEqual(result, expected)

    def test_get_yaml_lines_5(self):
        lines = self.construct_lines("\n---\nfoo: bar\n...\n\n---\nfoo: bar\n...\n")
        result = get_yaml_lines(lines)
        expected = ['foo: bar\n', 'foo: bar\n']
        self.assertEqual(result, expected)

    def test_get_yaml_lines_6(self):
        lines = self.construct_lines("\n---\nfoo: bar\n...\nasdlkaö sd\nasdasd asdasd\n---\nfoo: bar\n...\n")
        result = get_yaml_lines(lines)
        expected = ['foo: bar\n', 'foo: bar\n']
        self.assertEqual(result, expected)

    def test_get_yaml_1(self):
        result = get_input_yaml(self.markdown)
        self.assertTrue(result)
        self.assertTrue(STYLES_ in result)
        self.assertTrue('wiki' in result[STYLES_])
        self.assertEqual(result[STYLES_]['wiki'], 'tsihtml')

    def test_determine_style_1(self):
        options, _, _ = parse_cmdline(['--medium=wiki'])
        data = get_input_yaml(self.markdown)
        result = determine_style(options, data)
        expected = 'tsihtml'
        self.assertEqual(result, expected)

    def test_determine_style_2(self):
        options, _, _ = parse_cmdline([])
        data = get_input_yaml(self.markdown)
        result = determine_style(options, data)
        expected = None
        self.assertEqual(result, expected)

    def test_determine_style_3(self):
        options, _, _ = parse_cmdline(['--medium=pdf'])
        data = get_input_yaml(self.markdown)
        result = determine_style(options, data)
        expected = None
        self.assertEqual(result, expected)

    def test_determine_style_4(self):
        options, _, _ = parse_cmdline(['--medium=pdf'])
        data = get_input_yaml(self.markdown)
        data[STYLE_] = 'pdf'
        result = determine_style(options, data)
        expected = 'pdf'
        self.assertEqual(result, expected)

    def test_panache_styles_load_1(self):
        panache_styles = PanacheStyles()
        self.assertEqual(len(panache_styles.styles), 0)

    def test_panache_styles_load_2(self):
        panache_styles = PanacheStyles()
        panache_styles.load(self.style_dir)
        self.assertEqual(len(panache_styles.styles), 3)
        self.assertEqual(set(panache_styles.styles.keys()), {'html', 'en_html', 'it_html'})

    def test_panache_styles_update_1(self):
        panache_styles = PanacheStyles()
        panache_styles.load(self.style_dir)
        input_yaml = get_input_yaml(self.markdown)
        style_name = 'html'
        self.assertEqual(panache_styles.styles[style_name].metadata['lang'], 'en')
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], self.markdown)
        panache_styles.update(style)
        self.assertEqual(panache_styles.styles[style_name].metadata['lang'], 'ru')

    def test_panache_styles_resolve_1(self):
        panache_styles = PanacheStyles()
        panache_styles.load(self.style_dir)
        input_yaml = get_input_yaml(self.markdown)
        style_name = 'html'
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], self.markdown)
        panache_styles.update(style)
        expected = {'filter': [], 'metadata': {'lang': 'ru', 'foo': 'bar'}, 'commandline': {'toc': True}}
        result = panache_styles.resolve(style_name)
        self.assertEqual(result, expected)

    def testcompile_command_line_1(self):
        options, args, _ = parse_cmdline([])
        panache_styles = PanacheStyles()
        panache_styles.load(self.style_dir)
        input_yaml = get_input_yaml(self.markdown)
        style_name = 'html'
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], self.markdown)
        panache_styles.update(style)
        parameters = panache_styles.resolve(style_name)
        result = compile_command_line(self.markdown, 'foo/metadata', parameters, options, args)
        expected = ['pandoc', 'foo/metadata', self.markdown, '--toc']
        self.assertEqual(result, expected)

    def testcompile_command_line_2(self):
        style_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
        options, args, style_vars_dict = parse_cmdline(['--style-dir=%s' % style_dir, '--medium=wiki'])
        panache_styles = PanacheStyles()
        panache_styles.load(options.style_dir)
        input_yaml = get_input_yaml(self.markdown)
        style_name = determine_style(options, input_yaml)
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], self.markdown)
        panache_styles.update(style)
        parameters = panache_styles.resolve(style_name)
        parameters = substitute_style_vars(parameters, options, style_vars_dict)
        result = compile_command_line(self.markdown, 'foo/metadata', parameters, options, args)
        expected = {'pandoc', 'foo/metadata', self.markdown, '--toc-depth=3', '--number-sections',
                    '--highlight-style=tango', '--html-q-tags', '--smart', '--template=%s/template-html.html' % style_dir}
        self.assertEqual(set(result), expected)

if __name__ == '__main__':
    unittest.main()
