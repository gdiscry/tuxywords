# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Georges Discry
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
"""Clean the content of a file consisting of a list of words."""

from __future__ import print_function
import codecs
import sys
if sys.version_info[0] == 2:
    # Use the generator version of filter in Python 2
    from itertools import ifilter as filter


def is_valid(word):
    """Returns whether a given word is valid.

    A valid word does not start with an uppercase letter and does not contain
    an apostrophe.
    """
    if len(word) > 0 and word[0].isupper():
        return False
    if "'" in word:
        return False
    return True


def main():
    """Module entry point."""
    import argparse
    parser = argparse.ArgumentParser(
        description="""filters out words starting with an uppercase letters or
                       containing an apostrophe from a list of words""")
    # Cannot import the version from the package when running this module as a
    # script
    try:
        from . import __version__
        parser.add_argument('--version', action='version',
                            version='%(prog)s ' + __version__)
    except SystemError:
        pass
    parser.add_argument('source', type=argparse.FileType('rb'),
                        help='a file containing a list of words')
    parser.add_argument('destination', type=argparse.FileType('w'),
                        help='destination of the filtered list of words')
    args = parser.parse_args()
    # Decode the list of words as UTF-8 and remove the trailing \n
    words = (word.strip() for word in codecs.iterdecode(args.source, 'utf-8'))
    for word in filter(is_valid, words):
        print(word, file=args.destination)


if __name__ == '__main__':
    main()
