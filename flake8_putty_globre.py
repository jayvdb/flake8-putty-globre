# -*- coding: utf-8 -*-
"""Flake8 putty configuration."""
from __future__ import absolute_import, unicode_literals

import os

from flake8_putty.config import SelectorBase

import globre


class GlobRegexSelector(SelectorBase):

    """Regex selector."""

    _starts_with = './'

    def __init__(self, text=None):
        """Constructor."""
        self._compiled_regex = None
        super(GlobRegexSelector, self).__init__(text)

    @property
    def regex(self):
        """Return compiled regex."""
        if not self._compiled_regex:
            self._compiled_regex = globre.compile(self.raw)
        return self._compiled_regex

    def match(self, filename, line, codes):
        """Match selector against error parameters."""
        if not filename.startswith('.' + os.sep):
            filename = './' + filename

        if os.sep != '/':
            filename = filename.replace(os.sep, '/')

        return self.regex.search(filename)


SelectorBase.__implementations__.append(GlobRegexSelector)


class PuttyGlobRegexExtension(object):

    """Flake8 extension for adding filename glob support to putty."""

    name = 'flake8-putty-globre'
    version = '0.1'

    def __init__(self):
        """Constructor."""
        # Must exist for flake8 inspection of the extension
