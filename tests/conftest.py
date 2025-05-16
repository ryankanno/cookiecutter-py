#!/usr/bin/env python
#
# Copyright © 2022 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from itertools import product

import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture
def default_context(request: SubRequest) -> dict[str, str]:  # noqa: ARG001
    """Creates default prompt vals."""
    return {
        "author_name": "Ryan Kanno",
        "author_email": "ryankanno@localkinegrinds.com",
        "project_name": "Everybody go surf",
        "project_short_description": "This is a short description about {{ cookiecutter.project_name }}",  # noqa: B950, E501
        "project_url": "https://github.com/ryankanno/cookiecutter-py",
        "project_license": "MIT",
        "github_repository_owner": "ryankanno",
        "package_name": "surf",
        "version": "0.0.1",
        "python_version": "3.11",
        "supported_python_versions": "3.9, 3.10, 3.11, 3.12, pypy3.9, pypy3.10",  # noqa: B950, E501
        "uv_version": "0.0.1",
        "tox_version": "0.808.0",
        "sphinx_theme": "furo",
        "should_use_direnv": "y",
        "should_create_author_files": "y",
        "should_install_github_dependabot": "y",
        "should_automerge_autoapprove_github_dependabot": "y",
        "should_install_github_actions": "y",
        "should_upload_coverage_to_codecov": "y",
        "should_publish_to_pypi": "y",
    }


@pytest.fixture(params=list(product(['y', 'n'], repeat=6)))
def context(request: SubRequest) -> dict[str, str]:
    should_create_author_files = request.param[0]
    should_install_github_dependabot = request.param[1]
    should_automerge_autoapprove_github_dependabot = request.param[2]
    should_install_github_actions = request.param[3]
    should_publish_to_pypi = request.param[4]
    should_use_direnv = request.param[5]

    return {
        'author_name': 'Ryan',
        'author_email': 'ryankanno@localkinegrinds.com',
        'project_name': 'Test Project',
        'project_short_description': 'This is a test project',
        'project_url': 'https://github.com/ryankanno/cookiecutter-py',
        'project_license': 'MIT',
        'package_name': 'test_project',
        'version': '0.0.1',
        'python_version': '3.11',
        'supported_python_versions': '3.9, 3.10, 3.11, 3.12, pypy3.9, pypy3.10',  # noqa: B950, E501
        'should_use_direnv': should_use_direnv,
        'should_create_author_files': should_create_author_files,
        'should_install_github_dependabot': should_install_github_dependabot,
        "should_automerge_autoapprove_github_dependabot": should_automerge_autoapprove_github_dependabot,  # noqa: B950, E501
        'should_install_github_actions': should_install_github_actions,
        'should_upload_coverage_to_codecov': 'y',
        'should_publish_to_pypi': should_publish_to_pypi,
    }


# vim: fenc=utf-8
# vim: filetype=python
