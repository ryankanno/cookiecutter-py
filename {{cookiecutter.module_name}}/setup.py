#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


HERE = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(here, 'README.rst')) as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
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


with open(os.path.join(HERE, '{{ cookiecutter.module_name }}/__init__.py'), 'r') as f:
    for line in f:
        for pattern, handler in patterns.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))

# Requires

requires = []
tests_require = []
classifiers = []

setup(
    name='{{ cookiecutter.project.name }}',
    version=meta['VERSION'],
    description="{{ cookiecutter.project.short_description }}",
    long_description=readme + '\n\n' + history,
    author=meta['author'],
    author_email=meta['email'],
    url='{{ cookiecutter.project.url }}',
    packages=[
        '{{ cookiecutter.module_name }}',
    ],
    package_dir={'{{ cookiecutter.module_name }}':
                 '{{ cookiecutter.module_name }}'},
    include_package_data=True,
    install_requires=requires,
    license=meta['license'],
    zip_safe=False,
    keywords='{{ cookiecutter.module_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requires,
)

# vim: filetype=python
