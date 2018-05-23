# panache 

[![build-status](https://travis-ci.org/sebogh/panache.svg?branch=master)](https://travis-ci.org/sebogh/panache) 
[![codefactor](https://www.codefactor.io/repository/github/sebogh/panache/badge)](https://www.codefactor.io/repository/github/sebogh/panache) 
[![Known Vulnerabilities](https://snyk.io/test/github/sebogh/panache/badge.svg)](https://snyk.io/test/github/sebogh/panache)

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
single document may be converted to HTML as part of a Wiki, a draft HTML file
may be used while writing the document, and a standalone and self-contained
HTML-file may be send to a friend. At the same time, all version should be
rendered using the private style (as oposed to (for example) a company style).

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

Depending on the value of the command line option `--medium` (e.g. `darfthtml`,
`finalhtml`, or `wiki`), panache would select either the
`privatedrafthtml`-, `privatefinalhtml`- or `wikihtml`-style. It would then 
compute the commandline, filters and metadata for the selected style and finally 
call Pandoc.

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
      template: /home/sebastian/pandoc-templates/templates/wiki-de.html
---
```

to the previous `styledef_` or by adding it to a separate `styledef_` in another
file.

## Style Variables

Obviously, the style definitions above may work for the user `sebastian` but are
likely to fail for a different user. This is where parameterized style definitions
may be handy.

panache uses [{{ mustache }}](https://github.com/mustache/mustache.github.com)
as template engine. Through that, panache allows to use "tags" in style
definitions, wich are substituted based on commandline options and some
defaults. Using this, the above definition of the `germanwikihtml`-style may be
rewritten as follows:

```yaml
---
germanwikihtml:
  parent: wikihtml
  commandline:
      template: {{home}}/pandoc-templates/wiki-de.html
---
```

Now, if `--style-var=home:/home/sebastian` would be passed to
panache, then `template` would be resolved to 
`/home/sebastian/pandoc-templates/wiki-de.html` (and as
`--template=/home/sebastian/pandoc-templates/wiki-de.html` passed to Pandoc).
Obviously, using `--style-var=home:~` makes the panache call user agnostic
(in Bash).

Using regular [{{ mustache }}-syntax](http://mustache.github.io/mustache.5.html)
one may express conditions and repetitions.

# Installation

## Options

There are two options for using panache:

-   running the Python source
-   running a binary version

Both options will be described below.

## Python Source

Make sure the following requirements are satisfied:

-    [Pandoc] >= 2.0
-    Python >= 3.4 (incl. pyyaml, pystache)
-    \[git\]
-    \[virtualenv\]

Get `panache.py` by either:

-   getting the latest release from the [releases page] or
-   cloning the [github-repository]:

    ~~~~ {.bash}
    git clone https://github.com/sebogh/panache.git
    ~~~~

Run `panache.py`.

## Binary 

Make sure the following requirement is satisfied:

-    [Pandoc] >= 2.1

Dowload the latest binary from the [releases page] and run `panache.exe`
(Windows) or `panache` (Linux).

# Details

## Default Style- and Meta-Variables

The following Style- and Meta-Variables will be added by default, if input comes from STDIN:

| Variable                | Description                                                                                |
|------------------------ |--------------------------------------------------------------------------------------------|
| `panache_dir`           | directory of the panache script                                                            |
| `panache_version_X.Y.Z` | panache version where `X`, `Y`, `Z` are major, minor and patch (see [Semantic Versioning]) | 
| `os_X`                  | os type where `X` is one of `posix`, `nt`, `ce`, `java`.                                   | 
| `build_date`            | the date and time when panache was invoked (in the form `YYYY-mm-ddTHH:MM:SSZ`)            |

If input comes from a file the following additional Style- and Meta-Variables will be added by default:

| Variable                   | Description                                                                                |
|--------------------------- |--------------------------------------------------------------------------------------------|
| `input_dir`                | directory of the input file                                                                |
| `input_basename`           | basename of the input file                                                                 |
| `input_basename_root`      | basename without extension of the input file                                               |
| `input_basename_extension` | extension of the basename                                                                  |
| `vcsreference`             | vcs reference of the file                                                                  |
| `vcsdate`                  | vcs date (last change)                                                                     |


## MORE

tbd.


[releases page]: https://github.com/sebogh/panache/releases/latest
[github-repository]: https://github.com/sebogh/panache.git
[Pandoc]: https://pandoc.org
[panzer]: https://github.com/msprev/panzer
[Pandocomatic]: https://heerdebeer.org/Software/markdown/pandocomatic/
[Semantic Versioning]: https://semver.org/
