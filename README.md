# panache

## Overview

panache adds styles to [Pandoc]. 

The idea of panache is similar to that of [panzer] and [Pandocomatic]. It is yet
another Pandoc wrapper, that allows to assemble Pandoc-commandline options,
-metadata and -filter into styles. Through that, panache simplifies Pandoc calls
and ensures consistency across documents.

panache is similar to others in that cascading styles may be defined in separate
YAML-files and within documents.

panache is different in that its styles may contain variables and that documents
may specify multiple styles / context dependable styles.

## Context Dependable Styles

Often a Markdown document is the source for different targets. For example a
single document may be converted to HTML as part of a Wiki, a standalone HTML file
may be used locally, and a standalone and self-contained HTML-file may be send to
a friend. At the same time, all version should be rendered using the private
style (not the company one).

To address this situation, panache allows documents to specify multiple styles,
which get selected depending on a commandline option.

Assume, for example, a document with the following metadata-block:

```yaml
---
styles_:
  drafthtml: privatedrafthtml
  finalhtml: privatefinalhtml
  wiki: wikihtml
---
```

Depending on the command line option `--medium`, panache would select either the
`privatedrafthtml`-, `privatefinalhtml`- or `wikihtml`-style. It would compute
the commandline, filters and metadata for the selected style and finally call
Pandoc.

## Cascading Style Definition

panache allows to define styles in separate YAML-files and within documents. The
definition for a style with the name `wikihtml` might look like the following:

```yaml
---
styledef_:
  wikihtml:
    commandline:
      template: /home/sebastian/templates/wiki-en.html
    metadata:
      build-os: Linux
    filter:
      run: pandoc-citeproc
---
```

A second derived style, that changes the template, may be defined by adding:
    
```yaml
---
germanwikihtml:
  parent: wikihtml
  commandline:
      template: /home/sebastian/templates/wiki-de.html
---
```

to the `styledef_` above or by adding it to a separate `styledef_` in another
file.

## Style Variables

Obviously, the style definitions may work for the user `sebastian` but are
likely to produce unexpected results for a different user. That is where style
variables may be handy.

panache allows to use variables in style definitions, wich are (as of
"compiling" the final style) substituted based on commandline options. Using
this, the above definition of the `germanwikihtml`-style may be rewritten as
follows:

```yaml
---
germanwikihtml:
  parent: wikihtml
  commandline:
      template: ${template_dir}/wiki-de.html
---
```

Then, if (for example) `--style-var=template_dir:/foo` would be passed to
panache, then `template` would be resolved to `/foo/wiki-de.html` (and as
`--template=/foo/wiki-de.html` passed to Pandoc).

# Installation

## Options

There are two options for using panache:

-   running the Python source
-   running a binary version

Both options will be described below.

## Python Source

Make sure the following requirements are satisfied:

-    [Pandoc] >= 2.0
-    Python >= 3.4
-    \[git\]

Get `panache.py` by either:

-   getting the latest release from the [releases page] or
-   cloning the [github-repository]:

    ~~~~ {.bash}
    git clone https://github.com/sebogh/panache.git
    ~~~~

Run `panache.py`.

## Binary 

Make sure the following requirement is satisfied:

-    [Pandoc] >= 2.0

Dowload the latest binary from the [releases page] and run `panache.exe`
(Windows) or `panache` (Linux).

# Details

tbd.

[releases page]: https://github.com/sebogh/panache/releases
[github-repository]: https://github.com/sebogh/panache.git
[Pandoc]: https://pandoc.org
[panzer]: https://github.com/msprev/panzer
[Pandocomatic]: https://heerdebeer.org/Software/markdown/pandocomatic/
