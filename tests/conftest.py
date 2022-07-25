#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import pytest


@pytest.fixture()
def context():
    """Creates default prompt vals."""
    return {
        'author_name': 'Ryan',
        'author_email': 'ryankanno@localkinegrinds.com',
        'project_name': 'Test Project',
        'project_short_description': 'This is a test project',
        'project_url': 'https://github.com/ryankanno/cookiecutter-py',
        'project_license': 'MIT',
        'package_name': 'test_project',
        'version': '0.0.1',
        'python_version': '3.8',
        'should_create_author_files': 'y',
    }


# vim: fenc=utf-8
# vim: filetype=python
