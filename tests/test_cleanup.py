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

from tuxywords import cleanup


def test_is_valid():
    yield check_is_valid, u'abba'
    yield check_is_valid, u'épée'
    yield check_is_valid, u'hELLO'
    yield check_is_invalid, u'FOOBAR'
    yield check_is_invalid, u'Épée'
    yield check_is_invalid, u'Altux'
    yield check_is_invalid, u'TuxyMAT'
    yield check_is_invalid, u"it's"
    yield check_is_invalid, u"'apostrophe"
    yield check_is_invalid, u"apstrophe'"


def check_is_valid(word):
    assert cleanup.is_valid(word)


def check_is_invalid(word):
    assert not cleanup.is_valid(word)
