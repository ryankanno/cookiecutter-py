#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


HERE = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(HERE, 'README.rst')) as readme_file:
    readme = readme_file.read()


with open(os.path.join(HERE, 'HISTORY.rst')) as history_file:
    history = history_file.read().replace('.. :changelog:', '')

# Metadata

meta = {}
re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_version = re.compile(r'VERSION\s*=.*?\((.*?)\)')
strip_quotes = lambda s: s.strip("\"'")


def add_version(match):
    return {'VERSION': match.group(1).replace(" ", "").replace(",", ".")}


def add_meta(match):
    attr_name, attr_value = m.groups()
    return {attr_name: strip_quotes(attr_value)}


patterns = {
    re_meta: add_meta,
    re_version: add_version
}


relative_init_path = '{{ cookiecutter.module_name }}/__init__.py'
with open(os.path.join(HERE, relative_init_path), 'r') as f:
    for line in f:
        for pattern, handler in patterns.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))

# Tests

try:
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

        def initialize_options(self):
            TestCommand.initialize_options(self)
            self.pytest_args = []

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            import sys
            errno = pytest.main(self.pytest_args)
            sys.exit(errno)

except ImportError:
    from distutils.core import Command

    class PyTest(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            import subprocess
            import sys
            errno = subprocess.call([sys.executable, 'runtests.py'])
            raise SystemExit(errno)

# Requires

requires = []
tests_require = ['pytest']
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    "Programming Language :: Python :: 2",
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
]

setup(
    name='{{ cookiecutter.project_name }}',
    version=meta['VERSION'],
    description="{{ cookiecutter.project_short_description }}",
    long_description=readme + '\n\n' + history,
    url='{{ cookiecutter.project_url }}',
    author=meta['author'],
    author_email=meta['email'],
    license=meta['license'],
    classifiers=classifiers,
    keywords='{{ cookiecutter.module_name }}',
    packages=[
        '{{ cookiecutter.module_name }}',
    ],
    package_dir={'{{ cookiecutter.module_name }}':
                 '{{ cookiecutter.module_name }}'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    cmdclass={'test': PyTest},
    tests_require=tests_require,
)

# vim: filetype=python
