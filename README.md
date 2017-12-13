# armor

armor adds styles to Pandoc. 

armor was very much inspired by [panzer]. In fact, parts of it (e.g. some of the YAML-language) where shamelessly stolen from it. 

armor is different from panzer in that implements a "challenge response method". Through that, a Markdown document may specify different styles for the same target format (e.g. a draft HTML-style and a selfcontained HTML-style). The style that gets selected depends on the command line argument `--medium` -- the chalenge.

armor doesn't run Pandoc for style-processing. It's meant to be fast and impose as few overhead as possible.

armor doesn't support `preflight`, `postflight`, `postprocessor ` or `cleanup`. It simply compiles commandline, filters and metadata based on styles. 

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
