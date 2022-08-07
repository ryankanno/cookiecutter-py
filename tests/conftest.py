#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from itertools import product
import pytest


@pytest.fixture
def default_context(request):
    """Creates default prompt vals."""
    return {
        "author_name": "Ryan Kanno",
        "author_email": "ryankanno@localkinegrinds.com",
        "project_name": "Everybody go surf",
        "project_short_description": "This is a short description about {{ cookiecutter.project_name }}",  # noqa: B950
        "project_url": "https://github.com/ryankanno/cookiecutter-py",
        "project_license": "MIT",
        "github_repository_owner": "ryankanno",
        "package_name": "surf",
        "version": "0.0.1",
        "python_version": "3.8",
        "poetry_version": "1.1.14",
        "should_create_author_files": "y",
        "should_install_github_dependabot": "y",
        "should_install_github_actions": "y",
        "should_upload_coverage_to_codecov": "y",
        "should_publish_to_pypi": "y",
    }


@pytest.fixture(params=list(product(['y', 'n'], repeat=4)))
def context(request):

    should_create_author_files = request.param[0]
    should_install_github_dependabot = request.param[1]
    should_install_github_actions = request.param[2]
    should_publish_to_pypi = request.param[3]

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
        'should_upload_coverage_to_codecov': 'y',
        'should_publish_to_pypi': should_publish_to_pypi,
    }


# vim: fenc=utf-8
# vim: filetype=python
