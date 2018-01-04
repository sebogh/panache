#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest

script_dir = os.path.abspath(os.path.dirname(__file__)).replace(os.path.sep, '/')
base_dir = os.path.abspath(os.path.join(script_dir, '..')).replace(os.path.sep, '/')
resource_dir = '%s/resources' % script_dir
sample_markdown_file = '%s/sample.md' % resource_dir

sys.path.insert(1, base_dir)

from src.panache import \
    COMMANDLINE_, FILTER_, METADATA_, STYLEDEF_, STYLES_, \
    PanacheStyle, PanacheStyles, panache_yaml_format_variables, \
    parse_cmdline, get_yaml_lines, get_input_yaml, determine_style, compile_command_line, \
    substitute_style_vars_and_append_default


class SimpleTestCase(unittest.TestCase):

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
        result = get_input_yaml(sample_markdown_file)
        self.assertTrue(result)
        self.assertTrue(STYLES_ in result)
        self.assertTrue('wiki' in result[STYLES_])
        self.assertEqual(result[STYLES_]['wiki'], 'wikihtml')

    def test_parse_cmdline_1(self):
        _, _, style_vars = parse_cmdline(['--style-var=foo:bar'])
        self.assertTrue('foo' in style_vars)
        self.assertEqual(style_vars['foo'], 'bar')

    def test_parse_cmdline_2(self):
        _, _, style_vars = parse_cmdline(['--style-var=foo:bar', '--style-var=x:y'])
        self.assertTrue('foo' in style_vars)
        self.assertTrue('x' in style_vars)
        self.assertEqual(style_vars['foo'], 'bar')
        self.assertEqual(style_vars['x'], 'y')

    def test_parse_cmdline_3(self):
        _, _, style_vars = parse_cmdline(['--style-var=foo:bar', '--style-var=x:1', '--style-var=x:2'])
        self.assertTrue('foo' in style_vars)
        self.assertTrue('x' in style_vars)
        self.assertEqual(style_vars['foo'], 'bar')
        self.assertEqual(style_vars['x'], ['1', '2'])

    def test_parse_cmdline_4(self):
        _, args, _ = parse_cmdline(['--style-var=foo:bar'])
        self.assertFalse(args)

    def test_determine_style_1(self):
        options, _, _ = parse_cmdline(['--medium=wiki'])
        data = get_input_yaml(sample_markdown_file)
        result = determine_style(options, data)
        expected = 'wikihtml'
        self.assertEqual(result, expected)

    def test_determine_style_2(self):
        options, _, _ = parse_cmdline([])
        data = get_input_yaml(sample_markdown_file)
        result = determine_style(options, data)
        expected = None
        self.assertEqual(result, expected)

    def test_determine_style_3(self):
        options, _, _ = parse_cmdline(['--medium=pdf'])
        data = get_input_yaml(sample_markdown_file)
        result = determine_style(options, data)
        expected = None
        self.assertEqual(result, expected)


class AdvancedTestCase(unittest.TestCase):


    def setUp(self):
        logging.getLogger().setLevel(logging.ERROR)


    def test_panache_styles_load_1(self):
        panache_styles = PanacheStyles()
        self.assertEqual(len(panache_styles.styles), 0)

    def test_panache_styles_load_2(self):
        panache_styles = PanacheStyles()
        panache_styles.load(resource_dir)
        self.assertEqual(len(panache_styles.styles), 4)
        self.assertEqual(set(panache_styles.styles.keys()), {'html', 'en_html', 'it_html', 'wikihtml'})

    def test_panache_styles_update_1(self):
        panache_styles = PanacheStyles()
        panache_styles.load(resource_dir)
        input_yaml = get_input_yaml(sample_markdown_file)
        style_name = 'html'
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], sample_markdown_file)
        panache_styles.update(style)
        self.assertEqual(panache_styles.styles[style_name].metadata['lang'], 'ru')

    def test_panache_styles_resolve_1(self):
        panache_styles = PanacheStyles()
        panache_styles.load(resource_dir)
        input_yaml = get_input_yaml(sample_markdown_file)
        style_name = 'html'
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], sample_markdown_file)
        panache_styles.update(style)
        result = panache_styles.resolve(style_name)
        self.assertEqual(result[COMMANDLINE_], {'toc': True})
        self.assertEqual(result[FILTER_], [])
        self.assertEqual(result[METADATA_], {'lang': 'ru'})


    def testcompile_command_line_1(self):
        options, args, _ = parse_cmdline([])
        panache_styles = PanacheStyles()
        panache_styles.load(resource_dir)
        input_yaml = get_input_yaml(sample_markdown_file)
        style_name = 'html'
        style = PanacheStyle(style_name, input_yaml[STYLEDEF_][style_name], sample_markdown_file)
        panache_styles.update(style)
        parameters = panache_styles.resolve(style_name)
        result = compile_command_line(sample_markdown_file, 'foo/metadata', parameters, options, args)
        expected = ['pandoc', 'foo/metadata', sample_markdown_file, '--toc']
        self.assertEqual(result, expected)

    def testcompile_command_line_2(self):
        options, args, style_vars = parse_cmdline(['--style-dir=%s' % resource_dir, '--medium=wiki'])
        panache_styles = PanacheStyles(style_vars)
        panache_styles.load(options.style_dir)
        input_yaml = get_input_yaml(sample_markdown_file)
        style_name = determine_style(options, input_yaml)
        self.assertEqual(style_name, 'wikihtml')
        parameters = panache_styles.resolve(style_name)
        result = compile_command_line(sample_markdown_file, 'foo/metadata', parameters, options, args)
        expected = {'pandoc', 'foo/metadata', sample_markdown_file, '--toc', '--toc-depth=3', '--number-sections',
                    '--highlight-style=tango', '--html-q-tags', '--smart', '--template=%s/template-html.html' % resource_dir}
        self.assertEqual(set(result), expected)

if __name__ == '__main__':
    unittest.main()
