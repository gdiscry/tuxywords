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

from tuxywords import transform


def test_partitions():
    yield check_partitions, 'a', set([('', '')])
    yield check_partitions, 'lo', set([
        ('l', ''),
        ('', 'o'),
    ])
    yield check_partitions, 'foo', set([
        ('fo', ''),
        ('f', 'o'),
        ('', 'oo'),
    ])
    yield check_partitions, 'wxyz', set([
        ('', 'xyz'),
        ('w', 'yz'),
        ('wx', 'z'),
        ('wxy', ''),
    ])

def check_partitions(word, partitions):
    assert set(transform.RelationsBuilder.letter_partitions(word)) == partitions


def test_relations():
    yield check_relations, [], {}
    yield check_relations, ['foo'], {'foo': set(['foo'])}
    yield check_relations, ['ab', 'ac'], {
        'ab': set(['ab', 'ac']),
        'ac': set(['ab', 'ac']),
    }
    yield check_relations, ['ab', 'ac', 'bc', 'dd'], {
        'ab': set(['ab', 'ac']),
        'ac': set(['ab', 'ac', 'bc']),
        'bc': set(['ac', 'bc']),
        'dd': set(['dd']),
    }

def check_relations(wordlist, relations):
    builder = transform.RelationsBuilder(wordlist)
    assert builder.relations() == relations
