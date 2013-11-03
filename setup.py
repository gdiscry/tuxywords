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

from ez_setup import use_setuptools
use_setuptools('0.9.6')
from setuptools import setup

import codecs
import os
import re
import sys

# Path of the containing directory
here = os.path.dirname(os.path.abspath(__file__))

def read(*parts):
    """Return the content of the file at the given path."""
    with open(os.path.join(here, *parts), 'r') as f:
        return f.read()

def find_version(*file_paths):
    """Search an assignment to __version__ in the given file and return its value.

    The version string is obtained without importing the package or the module.
    This avoids dealing with the dependencies that are not yet installed.
    """
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = (?P<quote>['\"])([^'\"]*)(?P=quote)",
        version_file,
        re.M
    )
    if version_match:
        return version_match.group(2)
    raise RuntimeError("Unable to find version string.")

version = find_version('tuxywords', '__init__.py')

long_description = "\n".join([
    read('README.rst'),
    read('CHANGES.rst'),
])

setup(
    name='TuxyWORDS',
    version=version,
    description='A collection of scripts manipulating a list of words',
    long_description=long_description,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    author='Georges Discry',
    author_email='georges@discry.be',
    url='https://github.com/gdiscry/tuxywords',
    license='MIT',
    packages=[
        'tuxywords',
    ],
    entry_points={
        'console_scripts': [
            'twcleanup = tuxywords.cleanup:main',
        ],
    },
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
)
