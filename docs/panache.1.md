% PANACHE(1) panache user manual
% Sebastian Bogan
% 2017

# NAME

panache -- Pandoc wrapped in styles

# SYNOPSIS

panache [*OPTIONS*] [*PANDOC-OPTIONS*]

# DESCRIPTION

Pandoc wrapper implementing styles.

# OPTIONS

\--input=*PATH*
:   The input path. Default `STDIN`.The input path. Default `STDIN`.o

\--output=*PATH*
:   The output path. Default `STDOUT`.

\--medium=*MEDIUM*
:   The target medium.

\--style=*STYLE*
:   The fallback style to use, if --medium is not specified or the input 
    doesn't specify a style for the given medium.

\--style-dir=*PATH*
:   Where to find style definitions. (Default: `~/.panache`). 

\--style-var=*KEY*:*VALUE*
:   A variable that should be replaced in the style template.
    May be used several times. If the same key is used several 
    times, then the variable is interpreted as list of values.

\--disable-vcs-lookup
:   Don't try to get VCS reference and last change date.

\--verbose
:   Print verbose info (to `STDERR`).

\--debug
:   Print all debug info (to `STDERR`).

\--version
:   Print panache version info and exit.

\-h, --help
:   Print this help message.

# PANDOC-OPTIONS

Any argument not being one of the above options is passed down to Pandoc.

# AUTHORS

Copyright (c) 2017, Sebastian Bogan (sebogh@qibli.net).  Released under BSD
3-Clause "New" or "Revised" License.

# SEE ALSO

`pandoc` (1).
