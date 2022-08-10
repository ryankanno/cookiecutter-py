#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib.metadata


__title__ = '{{ cookiecutter.project_name }}'
__version__ = importlib.metadata.version(__package__ or __name__)
__author__ = '{{ cookiecutter.author_name }}'
__email__ = '{{ cookiecutter.author_email }}'
__license__ = '{{ cookiecutter.project_license }}'
# fmt: off
__copyright__ = "Copyright (c) {% now 'utc', '%Y' %}, {{cookiecutter.author_name}}"
# fmt: on


# vim: fenc=utf-8
# vim: filetype=python
