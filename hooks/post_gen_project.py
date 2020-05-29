#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import os
from distutils.util import strtobool

PROJECT_ROOT_DIR = os.path.realpath(os.path.curdir)


def remove_file(fp):
    os.remove(os.path.join(PROJECT_ROOT_DIR, fp))


def manage_author_files(should_create_author_files):
    if not strtobool(should_create_author_files):
        remove_file('AUTHORS.rst')


if __name__ == '__main__':
    manage_author_files('{{ cookiecutter.should_create_author_files }}')


# vim: fenc=utf-8
# vim: filetype=python
