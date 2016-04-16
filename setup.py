#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Flake8 putty globre setup module."""
from __future__ import absolute_import, unicode_literals, with_statement

from setuptools import setup

setup(
    name='flake8-putty-globre',
    version='0.1',
    description='Add globre support to flake8-putty.',
    long_description='Allow use of globs in filename matching',
    keywords='flake8 pep8 putty glob',
    author='John Vandenberg',
    author_email='jayvdb@gmail.com',
    url='https://github.com/jayvdb/flake8-putty-ignore',
    install_requires=[
        'flake8-putty',
        'globre',
    ],
    license='MIT',
    py_modules=[str('flake8_putty_globre')],
    entry_points={
        'flake8.extension': [
            'flake8_putty_globre = flake8_putty_globre:PuttyGlobRegexExtension',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
