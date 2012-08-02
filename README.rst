=======
whoyeah
=======
a grep like text finder in Python

Usage: whoyeah.py [options] PATTERN

Options
  -h, --help            show this help message and exit
  -i, --ignore_case     ignore case sensitive
  -t TARGET, --target=TARGET
                        set search target
  -q BIGFILE, --quiet=BIGFILE
                        ignore file or directory to be search
  -s NEW_STRING, --replace=NEW_STRING
                        replace by new string

Inspired
========
* grep-ack - a perl grep-like
* grin from http://pypi.python.org/pypi/grin for is_binary()

Feature
=======
* summery count result
* colorful
* ignore binary
* customize ignore list: .wyignore

TODO
====
* speed up, grep and ack-grep is much more faster
* find in type (file extension, c, h, mk)
* find in certein files
* stdin
