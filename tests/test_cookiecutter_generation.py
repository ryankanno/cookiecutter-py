#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Tests project generation."""

import logging
import mmap
import os
import re
import typing
from distutils.util import strtobool
from pathlib import Path

import pytest
from binaryornot.check import is_binary
from pytest_cookies.plugin import Cookies


LOGGER = logging.getLogger(__name__)
PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


EXPECTED_BASE_BAKED_FILES = [
    '.commitlint.config.js',
    '.dockerignore',
    '.gitignore',
    '.konchrc',
    '.pre-commit-config.yaml',
    '.secrets.baseline',
    'Dockerfile',
    'docker-entrypoint.sh',
    'HISTORY.rst',
    'LICENSE',
    'Justfile',
    'README.md',
    '/docs/Makefile',
    '/docs/conf.py',
    '/docs/index.rst',
    '/docs/make.bat',
    '/docs/_static/.keep',
    '/docs/getting_started/getting_started.rst',
    '/docs/roadmap/roadmap.rst',
    '/docs/todo/todo.rst',
    '/docs/usage/usage.rst',
    'logging.yaml',
    'poetry.lock',
    'pyproject.toml',
    'tox.ini',
    '_typos.toml',
]

EXPECTED_BAKED_DIRENV_FILES = ['.envrc']

EXPECTED_BAKED_AUTHORS_FILES = [
    'AUTHORS.rst',
]

EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES = [
    '/.github/dependabot.yml',
]

EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES = [
    '/.github/workflows/auto-approve-merge-dependabot.yml',
]

EXPECTED_BAKED_GITHUB_ACTIONS_FILES = [
    '/.github/labeler.yml',
    '/.github/release-drafter.yml',
    '/.github/workflows/ci.yml',
    '/.github/workflows/codeql-analysis.yml',
    '/.github/workflows/commitlint.yml',
    '/.github/workflows/docs.yml',
    '/.github/workflows/hadolint.yml',
    '/.github/workflows/pr-labeler.yml',
    '/.github/workflows/pr-size-labeler.yml',
    '/.github/workflows/release-drafter.yml',
    '/.github/workflows/trufflehog.yml',
]

EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES = [
    '/.github/workflows/publish.yml',
]


def get_expected_baked_files(package_name: str) -> typing.List[str]:
    return EXPECTED_BASE_BAKED_FILES + [
        f'/{package_name}/__init__.py',
        f'/{package_name}/{package_name}.py',
        '/tests/__init__.py',
        f'/tests/test_{package_name}.py',
    ]


def build_files_list(
    root_dir: str, is_absolute: bool = True
) -> typing.List[str]:
    """Build a list containing abs/relative paths to the generated files."""
    return [
        (
            str(Path(dirpath) / file_path)
            if is_absolute
            else str(Path(dirpath[len(root_dir) :]) / file_path)
        )
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths_substitution(paths: typing.List[str]) -> None:
    for path in paths:
        if is_binary(path):
            continue
        with Path(path).open(encoding="utf-8") as f:
            line = f.readline()
            match = RE_OBJ.search(line)
            assert (
                match is None
            ), f"cookiecutter variable not replaced in {path}"


def check_paths_exist(
    expected_paths: typing.List[str], baked_files: typing.List[str]
) -> None:
    baked_files_no_pycache = filter(
        lambda x: '__pycache__' not in x, baked_files
    )

    baked_files_no_ruff = filter(
        lambda x: '.ruff_cache' not in x, list(baked_files_no_pycache)
    )

    expected_baked_files = list(baked_files_no_ruff)

    assert len(expected_paths) == len(expected_baked_files)

    for expected_path in expected_paths:
        assert expected_path in expected_baked_files


def test_with_default_configuration(
    cookies: Cookies, default_context: typing.Dict[str, str]
) -> None:
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))
    assert abs_baked_files
    check_paths_substitution(abs_baked_files)

    rel_baked_files = build_files_list(
        str(baked_project.project_path), is_absolute=False
    )
    assert rel_baked_files

    expected_files = (
        get_expected_baked_files(default_context['package_name'])
        + EXPECTED_BAKED_AUTHORS_FILES
        + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES
        + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
        + EXPECTED_BAKED_DIRENV_FILES
        + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
        + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
    )

    check_paths_exist(expected_files, rel_baked_files)


def test_with_parameterized_configuration(  # noqa: C901, PLR0912, PLR0915
    cookies: Cookies, context: typing.Dict[str, str]
) -> None:
    if not bool(strtobool(context['should_install_github_dependabot'])):
        context['should_automerge_autoapprove_github_dependabot'] = 'n'

    if not bool(strtobool(context['should_install_github_actions'])):
        context['should_automerge_autoapprove_github_dependabot'] = 'n'

    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))
    assert abs_baked_files
    check_paths_substitution(abs_baked_files)

    rel_baked_files = build_files_list(
        str(baked_project.project_path), is_absolute=False
    )
    assert rel_baked_files

    LOGGER.info("author file: %s", context['should_create_author_files'])
    LOGGER.info("dependabot: %s", context['should_install_github_dependabot'])
    LOGGER.info(
        "automerge_autoapprove_dependabot: %s",
        context['should_automerge_autoapprove_github_dependabot'],
    )
    LOGGER.info("gh actions: %s", context['should_install_github_actions'])
    LOGGER.info("pypi: %s", context['should_publish_to_pypi'])
    LOGGER.info("direnv: %s", context['should_use_direnv'])

    expected_files = get_expected_baked_files(context['package_name'])

    if strtobool(context['should_create_author_files']):
        expected_files += EXPECTED_BAKED_AUTHORS_FILES

    if strtobool(context['should_publish_to_pypi']):
        expected_files += EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES

    if strtobool(context['should_install_github_dependabot']):
        expected_files += EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES

    if strtobool(context['should_use_direnv']):
        expected_files += EXPECTED_BAKED_DIRENV_FILES

    if strtobool(context['should_install_github_actions']):
        if strtobool(
            context['should_automerge_autoapprove_github_dependabot']
        ):  # noqa: B950
            check_paths_exist(
                expected_files
                + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
                rel_baked_files,
            )
        else:
            check_paths_exist(
                expected_files + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
                rel_baked_files,
            )
    elif not strtobool(context['should_install_github_actions']):
        check_paths_exist(
            list(
                set(expected_files)
                - set(EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES)
            ),
            rel_baked_files,
        )
    else:
        pytest.fail('eeps. missed a case')


@pytest.mark.parametrize('codecov', ['y', 'n'])
def test_with_codecov(
    cookies: Cookies, default_context: typing.Dict[str, str], codecov: str
) -> None:
    default_context['should_upload_coverage_to_codecov'] = codecov
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'ci.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if s.find(b'codecov') == -1 and codecov == 'y':
                    pytest.fail('Should have codecov')
                elif s.find(b'codecov') != -1 and codecov == 'n':
                    pytest.fail('Should not have codecov')


@pytest.mark.parametrize('poetry_version', ['8.0.8', '4.2.0'])
def test_with_poetry_version(
    cookies: Cookies,
    default_context: typing.Dict[str, str],
    poetry_version: str,
) -> None:
    default_context['poetry_version'] = poetry_version
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'Dockerfile' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if s.find(f"POETRY_VERSION={poetry_version}".encode()) == -1:
                    pytest.fail('Should have appropriate poetry version')


@pytest.mark.parametrize('tox_version', ['8.0.8', '4.2.0'])
def test_with_tox_version(
    cookies: Cookies,
    default_context: typing.Dict[str, str],
    tox_version: str,
) -> None:
    default_context['tox_version'] = tox_version
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'ci.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if s.find(f"tox=={tox_version}".encode()) == -1:
                    pytest.fail('Should have appropriate tox version')


@pytest.mark.parametrize('version', ['42.0', '4.2.0'])
def test_with_version(
    cookies: Cookies,
    default_context: typing.Dict[str, str],
    version: str,
) -> None:
    default_context['version'] = version
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'pyproject.toml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if s.find(f"version = {version!r}".encode()) == -1:
                    pytest.fail(
                        'pyproject.toml should have appropriate version'
                    )


def test_pyproject_with_default_configuration(
    cookies: Cookies,
    default_context: typing.Dict[str, str],
) -> None:
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'pyproject.toml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if s.find(b'[tool.mypy]') == -1:
                    pytest.fail('Should have mypy configuration section')
                if s.find(b'[tool.ruff.lint]') == -1:
                    pytest.fail('Should have ruff lint configuration')

                for line in iter(s.readline, b""):
                    trim_line = line.decode().strip()
                    if trim_line.startswith('# python'):
                        pytest.fail('Should not have commented out python')


# vim: fenc=utf-8
# vim: filetype=python
