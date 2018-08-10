#!/usr/bin/env python

from setuptools import setup

setup(
    name='SWHE',
    version='0',
    author="Matt Mitchell",
    author_email="mitchute@gmail.com",
    packages=['swhe'],
    long_description=open('README.md').read(),
    test_suite='nose.collector',
    tests_require=['nose']
)
