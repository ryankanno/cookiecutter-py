"""
Tests project generation
"""

import os
import re

from distutils.util import strtobool
from typing import List

from binaryornot.check import is_binary
import pytest


PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


EXPECTED_BASE_BAKED_PROJECT_FILES = [
    '.commitlint.config.js',
    '.coveragerc',
    '.dockerignore',
    '.flake8',
    '.gitignore',
    '.konchrc',
    '.pre-commit-config.yaml',
    'Dockerfile',
    'HISTORY.rst',
    'LICENSE',
    'Makefile',
    'README.rst',
    '/docs/Makefile',
    '/docs/conf.py',
    '/docs/index.rst',
    '/docs/make.bat',
    'logging.yaml',
    'pyproject.toml',
    'pytest.ini',
    'setup.cfg',
    '/test_project/__init__.py',
    '/test_project/test_project.py',
    '/tests/test_test_project.py',
    'tox.ini',
]

EXPECTED_BAKED_AUTHORS_FILES = [
    'AUTHORS.rst',
]

EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES = [
    '/.github/dependabot.yml',
]

EXPECTED_BAKED_GITHUB_ACTIONS_FILES = [
    '/.github/labeler.yml',
    '/.github/workflows/ci.yml',
    '/.github/workflows/codeql-analysis.yml',
    '/.github/workflows/commitlint.yml',
    '/.github/workflows/hadolint.yml',
    '/.github/workflows/pr-labeler.yml',
    '/.github/workflows/pr-size-labeler.yml',
]


def build_files_list(root_dir: str, is_absolute: bool = True) -> List[str]:
    """Build a list containing abs/relative paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        if is_absolute
        else os.path.join(dirpath[len(root_dir) :], file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths_substitution(paths):
    for path in paths:
        if is_binary(path):
            continue
        for line in open(path):
            match = RE_OBJ.search(line)
            assert (
                match is None
            ), f"cookiecutter variable not replaced in {path}"


def check_paths_exist(
    expected_paths: List[str], baked_files: List[str]
) -> None:
    assert len(expected_paths) == len(baked_files)

    for _, expected_path in enumerate(expected_paths):
        assert expected_path in baked_files


def test_with_default_configuration(cookies, context):

    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))
    assert abs_baked_files
    check_paths_substitution(abs_baked_files)

    rel_baked_files = build_files_list(
        str(baked_project.project_path), is_absolute=False
    )
    assert rel_baked_files

    if (
        strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            EXPECTED_BASE_BAKED_PROJECT_FILES
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and not strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            EXPECTED_BASE_BAKED_PROJECT_FILES
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES,
            rel_baked_files,
        )
    elif (
        strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            EXPECTED_BASE_BAKED_PROJECT_FILES
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            EXPECTED_BASE_BAKED_PROJECT_FILES
            + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            EXPECTED_BASE_BAKED_PROJECT_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and not strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(EXPECTED_BASE_BAKED_PROJECT_FILES, rel_baked_files)
