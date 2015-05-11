#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'patch'))


VERSION = version_info(0, 0, 1)


__title__ = '{{ cookiecutter.project_name }}'
__version__ = '{0.major}.{0.minor}.{0.patch}'.format(VERSION)
__author__ = '{{ cookiecutter.author_name }}'
__email__ = '{{ cookiecutter.author_email }}'
__license__ = '{{ cookiecutter.project_license }}'
__copyright__ = 'Copyright {{ cookiecutter.year }} {{ cookiecutter.author_name }}'

# vim: filetype=python
