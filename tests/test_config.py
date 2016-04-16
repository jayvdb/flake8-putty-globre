# -*- coding: utf-8 -*-
"""Test config parser."""
from __future__ import absolute_import, unicode_literals

import os

from unittest import TestCase

from flake8_putty.config import (
    FileSelector,
    Parser,
    Rule,
)

from flake8_putty_globre import GlobRegexSelector


class TestParser(TestCase):

    """Test config option rule parser."""

    def test_selector_globre(self):
        p = Parser('./foo : E101')
        assert list(p._lines()) == [
            (1, './foo : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./foo'], 'E101'),
        ]

        assert p._rules == [
            Rule([GlobRegexSelector('./foo')], 'E101'),
        ]

    def test_selector_globre_multi(self):
        p = Parser('./foo, ./bar : E101')
        assert list(p._lines()) == [
            (1, './foo, ./bar : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./foo', './bar'], 'E101'),
        ]

        assert p._rules == [
            Rule(
                [GlobRegexSelector('./foo'), GlobRegexSelector('./bar')],
                'E101',
            ),
        ]

    def test_selector_mixed(self):
        p = Parser('./foo, bar.py : E101')
        assert list(p._lines()) == [
            (1, './foo, bar.py : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./foo', 'bar.py'], 'E101'),
        ]

        assert p._rules == [
            Rule(
                [GlobRegexSelector('./foo'), FileSelector('bar.py')],
                'E101',
            ),
        ]

    def test_selector_mixed_after(self):
        p = Parser('bar.py , ./foo : E101')
        assert list(p._lines()) == [
            (1, 'bar.py , ./foo : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['bar.py', './foo'], 'E101'),
        ]

        assert p._rules == [
            Rule(
                [FileSelector('bar.py'), GlobRegexSelector('./foo')],
                'E101',
            ),
        ]

    def test_selector_filename_explicit_relative(self):
        p = Parser('./foo.py : E101')
        assert list(p._lines()) == [
            (1, './foo.py : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./foo.py'], 'E101'),
        ]

        assert p._rules == [
            Rule([GlobRegexSelector('./foo.py')], 'E101'),
        ]

    def test_selector_explicit_relative_dir(self):
        p = Parser('./ : E101')
        assert list(p._lines()) == [
            (1, './ : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./'], 'E101'),
        ]

        assert p._rules == [
            Rule([GlobRegexSelector('./')], 'E101'),
        ]

    def test_selector_explicit_relative_star(self):
        p = Parser('./* : E101')
        assert list(p._lines()) == [
            (1, './* : E101'),
        ]

        assert list(p._parsed_lines()) == [
            (1, ['./*'], 'E101'),
        ]

        assert p._rules == [
            Rule([GlobRegexSelector('./*')], 'E101'),
        ]


class TestMatch(TestCase):

    """Test config option rule parser."""

    def test_selector_filename(self):
        p = Parser('./foo.py : E101')
        assert p._rules[0].match('foo.py', 1, 'x')
        assert p._rules[0].match('.{0}foo.py'.format(os.sep), 1, 'x')
        assert not p._rules[0].match('bar.py', 1, 'x')
        assert not p._rules[0].match('foo/bar.py', 1, 'x')

    def test_selector_filename_multi(self):
        p = Parser('./foo.py, ./bar.py : E101')
        assert p._rules[0].file_match_any('foo.py')
        assert p._rules[0].file_match_any('.{0}foo.py'.format(os.sep))
        assert p._rules[0].file_match_any('bar.py')
        assert not p._rules[0].file_match_any('foo/bar.py')

    def test_selector_directory(self):
        p = Parser('./tests/ : E101')
        assert p._rules[0].file_match_any('tests/foo.py')
        assert not p._rules[0].file_match_any('other/foo.py')

    def test_selector_directory_multi(self):
        p = Parser('./tests/, ./vendor/ : E101')
        assert p._rules[0].file_match_any('tests/foo.py')
        assert p._rules[0].file_match_any('vendor/foo.py')
        assert not p._rules[0].file_match_any('other/foo.py')

    def test_selector_directory_wildcard(self):
        p = Parser('./tests/**/test_*.py : E101')
        assert p._rules[0].file_match_any('tests/foo/test_bar.py')
        assert p._rules[0].file_match_any(
            '.{0}tests/foo/bar/test_baz.py'.format(os.sep),
        )
        assert p._rules[0].file_match_any('tests/foo/bar/test_.py')
        assert not p._rules[0].file_match_any('tests/test_foo.py')

    def test_selector_directory_wildcard_nested(self):
        p = Parser('./tests/*/*/test_*.py : E101')
        assert p._rules[0].file_match_any('tests/foo/bar/test_baz.py')
        assert not p._rules[0].file_match_any('tests/foo/test_bar.py')

    def test_selector_directory_wildcard_multi(self):
        p = Parser('./tests/*/test_*.py, ./vendor/*/test_*.py : E101')
        assert p._rules[0].file_match_any('tests/foo/test_bar.py')
        assert p._rules[0].file_match_any('vendor/foo/test_bar.py')
        assert not p._rules[0].file_match_any('other/foo/test_bar.py')

    def test_selector_directory_wildcard_multi_non_glob(self):
        p = Parser('./tests/*/test_*.py, vendor/*/test_*.py : E101')
        assert not p._rules[0].file_match_any('tests/foo/test_bar.py')
        assert not p._rules[0].file_match_any('vendor/foo/test_bar.py')
        assert not p._rules[0].file_match_any('tests/vendor/foo/test_bar.py')
