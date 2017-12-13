# armor

armor adds styles to Pandoc. 

armor was very much inspired by [panzer]. In fact, parts of it (e.g. some of the YAML-language) where shamelessly stolen from it. 

armor is different from panzer in that implements a kind of "challenge response method". Through that, a Markdown document may specify "context-dependend" styles.

Assume, for example, a document with the following Pandoc metadata-block:

```yaml
---
styles_:
  drafthtml: mydrafthtml
  finalhtml: myfinalhtml
  wiki: wikihtml
---
```

Then, depending on command line option `--medium`, armor would select either the `drafthtml`-, `finalhtml`- or `wikihtml`-style. It would compute the commandline, filters and metadata for the selected style (from external YAML files and style-definitions inside the input document) and finally call Pandoc.

armor doesn't run Pandoc for style-processing. It's meant to be fast and impose as few overhead as possible.

armor doesn't support `preflight`, `postflight`, `postprocessor ` or `cleanup`. 

armor adds style variables. 

# Installation

Requirements:

-    [Pandoc] >= 2.0
-    [Python] >= 3.5 (inkl. `pip`)

````bash
pip3 install git+https://github.com/sebogh/armor
````

[Pandoc]: https://pandoc.org/
[Python]: https://www.python.org/downloads/
[panzer]: https://github.com/msprev/panzer
