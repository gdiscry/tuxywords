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
"""Transforms words into other words by changing one letter at a time."""

import codecs

from collections import defaultdict, deque
from gettext import gettext as _


class RelationsBuilder(object):
    """Constructs the relations between a set of words.

    There is a relation between two words if we can transform one word into the
    other by changing one of its letters.
    """

    @staticmethod
    def letter_partitions(word):
        """Generates the partitions of a word formed by removing each of its
        letters.

        A partition is a tuple containing the prefix and the suffix of the word
        surrounding the removed letter. The partitions of 'foo' are ('', 'oo'),
        ('f', 'o') and ('fo', '').
        """
        length = len(word)
        for i in range(length):
            yield (word[0:i], word[i+1:length])

    def __init__(self, words=None):
        """Creates a new builder that establishes the relations between words.

        words is an iterable that contains the initial list of words for which
        we want to establish the relations.
        """
        self._relations = defaultdict(set)
        if words is not None:
            for word in words:
                self.connect(word)

    def connect(self, word):
        """Computes the relations of the given word with the words that were
        previously added.
        """
        for partition in self.letter_partitions(word):
            # Group together the words having a common partition
            self._relations[partition].add(word)

    def relations(self):
        """Returns a dictionnary that maps a word with the set of words with
        which it has a relation.
        """
        graph = defaultdict(set)
        for relation in self._relations.values():
            for word in relation:
                graph[word] |= relation
        return graph


class NoTransformationError(Exception):
    """Exception raised when no transformation is possible between two words.
    """
    pass


class TransformationFinder(object):
    """Finds the shortest list of transformations between elements based on the
    relations existing between them.
    """

    def __init__(self, relations):
        self.relations = relations

    def find_transformation(self, start, end):
        """Finds the shortest list of transformations between the start and end
        elements.
        """
        next_transformation = {end: None}
        boundary = deque([end])
        # Iterates over the boundary of elements with a known transformation
        # that are connected to elements with an unknown transformation
        def iter_boundary():
            try:
                while True:
                    yield boundary.popleft()
            except IndexError:
                pass
        for pos, word in enumerate(iter_boundary()):
            for relation in self.relations[word]:
                # Ignore words with a known transformation
                if relation not in next_transformation:
                    next_transformation[relation] = word
                    if relation == start:
                        break
                    else:
                        boundary.append(relation)
        if start not in next_transformation:
            # The start and end elements are not related
            raise NoTransformationError()
        word = start
        while word is not None:
            yield word
            word = next_transformation[word]


class NormalizedWordList(object):
    """A generator that normalizes and filters a list of words from an
    iterator.

    It also checks for the existence of specific words during the iteration.
    """

    def __init__(self, wordlist, wordlength, must_contain=None):
        """Creates a normalized word list based on the contents of wordlist.

        Only words that have a length of wordlength are kept and the existence
        of the words given in must_contain is checked.
        """
        self.iterwords = codecs.iterdecode(wordlist, 'utf-8')
        self.wordlength = wordlength
        self.contains = {}
        if must_contain is not None:
            for word in must_contain:
                self.contains[word] = False

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            word = next(self.iterwords).strip()
            if word in self.contains:
                self.contains[word] = True
            if len(word) == self.wordlength:
                return word

    # Python 2 compatibility
    next = __next__


def main():
    """Module entry point."""
    import argparse
    parser = argparse.ArgumentParser(
        description="""transforms a word into another word by changing one
                       letter at a time """)
    # Cannot import the version from the package when running this module as a
    # script
    try:
        from . import __version__
        parser.add_argument('--version', action='version',
                            version='%(prog)s ' + __version__)
    except SystemError:
        pass
    # Work around the encoding differences between Python 2 and 3 for the
    # command-line arguments
    import sys
    if sys.version_info[0] == 3:
        word_type = str
    else:
        def word_type(object):
            return unicode(object, 'utf-8')
    parser.add_argument('--from', dest='start', required=True, type=word_type,
                        help='word to transform from')
    parser.add_argument('--to', dest='end', required=True, type=word_type,
                        help='word to transform to')
    parser.add_argument('wordlist', type=argparse.FileType('rb'),
                        help='a file containing a list of words')
    args = parser.parse_args()
    # The words in the chain of transformations must have the same length
    if len(args.start) != len(args.end):
        parser.error('the --from and --to arguments must have the same length')
    # Filter and normalize the words and check for the presence of the words at
    # the beginning and end of the transformation (the check is valid once the
    # iteration is finished)
    words = NormalizedWordList(args.wordlist, len(args.start),
                               must_contain=[args.start, args.end])
    relations = RelationsBuilder(words).relations()
    if not words.contains[args.start]:
        parser.exit(1, _('%s: error: %s\n') % (parser.prog,
                       "'%s' is not in the list of words" % args.start))
    if not words.contains[args.end]:
        parser.exit(1, _('%s: error: %s\n') % (parser.prog,
                       "'%s' is not in the list of words" % args.start))
    try:
        finder = TransformationFinder(relations)
        for word in finder.find_transformation(args.start, args.end):
            print(word)
    except NoTransformationError:
        parser.exit(1, _('%s: error: %s\n') % (parser.prog,
                       "no transformation is possible from '%s' to '%s'" %
                       (args.start, args.end)))


if __name__ == '__main__':
    main()
