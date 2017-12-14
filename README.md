# panache

panache adds styles to Pandoc. 

panache was very much inspired by [panzer]. In fact, parts of it (e.g. some of the YAML-language) where shamelessly stolen from it. 

panache is different from panzer in that implements a kind of "challenge response method". Through that, a Markdown document may specify "context-dependend" styles. Assume, for example, a document with the following Pandoc metadata-block:

```yaml
---
styles_:
  drafthtml: privatedrafthtml
  finalhtml: privatefinalhtml
  wiki: wikihtml
---
```

Then, depending on command line option `--medium`, panache would select either the `privatedrafthtml`-, `privatefinalhtml`- or `wikihtml`-style. It would compute the commandline, filters and metadata for the selected style (from external YAML files and style-definitions inside the input document) and finally call Pandoc.

panache doesn't run Pandoc for style-processing. It's meant to be fast and impose as few overhead as possible.

panache doesn't support `preflight`, `postflight`, `postprocessor ` or `cleanup`. 

panache adds style variables, which are substituted before handing over to Pandoc. For a style defined as: 

```yaml
---
styledef_:
  wikihtml:
    commandline:
      data-dir: ${style_dir}/blub
    metadata:
      build-os: ${build_os}
---
```

and an panache call like `panache.py --style-dir=/foo --stylevar=build_os:Linux`, `${style_dir}` and `${build_os}` would be replaced by `/foo` and `Linux` respectively. This, would then lead to the Pandoc commandline option `--data-dir=/foo/blub` and a metavariable `${build-os}` with the value `Linux`.


# Installation

Requirements:

-    [Pandoc] >= 2.0
-    [Python] >= 3.5 (inkl. `pip`)

````bash
pip3 install git+https://github.com/sebogh/panache
````

[Pandoc]: https://pandoc.org/
[Python]: https://www.python.org/downloads/
[panzer]: https://github.com/msprev/panzer
