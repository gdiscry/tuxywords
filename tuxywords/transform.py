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

from collections import defaultdict, deque


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
