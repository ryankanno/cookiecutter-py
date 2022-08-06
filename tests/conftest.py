#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import pytest


@pytest.fixture(
    params=[
        ('y', 'y', 'y'),
        ('y', 'y', 'n'),
        ('y', 'n', 'y'),
        ('n', 'y', 'y'),
        ('n', 'n', 'y'),
        ('n', 'n', 'n'),
    ]
)
def context(request):

    should_create_author_files = request.param[0]
    should_install_github_dependabot = request.param[1]
    should_install_github_actions = request.param[2]

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
        'should_create_author_files': should_create_author_files,
        'should_install_github_dependabot': should_install_github_dependabot,
        'should_install_github_actions': should_install_github_actions,
    }


# vim: fenc=utf-8
# vim: filetype=python
