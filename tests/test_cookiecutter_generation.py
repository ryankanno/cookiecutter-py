#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""
Tests project generation
"""

import mmap
import os
import re
import typing
from distutils.util import strtobool

import pytest
from binaryornot.check import is_binary
from pytest_cookies.plugin import Cookies


PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


EXPECTED_BASE_BAKED_FILES = [
    '.bandit',
    '.commitlint.config.js',
    '.dockerignore',
    '.flake8',
    '.gitignore',
    '.konchrc',
    '.pre-commit-config.yaml',
    '.secrets.baseline',
    'bandit.yaml',
    'Dockerfile',
    'docker-entrypoint.sh',
    'HISTORY.rst',
    'LICENSE',
    'Makefile',
    'README.rst',
    '/docs/Makefile',
    '/docs/conf.py',
    '/docs/index.rst',
    '/docs/make.bat',
    'logging.yaml',
    'poetry.lock',
    'pyproject.toml',
    'tox.ini',
]

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


def get_expected_baked_default_files(package_name: str) -> typing.List[str]:
    return (
        get_expected_baked_files(package_name)
        + EXPECTED_BAKED_AUTHORS_FILES
        + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
        + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
        + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
        + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES
    )


def build_files_list(
    root_dir: str, is_absolute: bool = True
) -> typing.List[str]:
    """Build a list containing abs/relative paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        if is_absolute
        else os.path.join(dirpath[len(root_dir) :], file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths_substitution(paths: typing.List[str]) -> None:
    for path in paths:
        if is_binary(path):
            continue
        for line in open(path):
            match = RE_OBJ.search(line)
            assert (
                match is None
            ), f"cookiecutter variable not replaced in {path}"


def check_paths_exist(
    expected_paths: typing.List[str], baked_files: typing.List[str]
) -> None:

    baked_files_no_pycache = list(
        filter(lambda x: '__pycache__' not in x, baked_files)
    )

    assert len(expected_paths) == len(baked_files_no_pycache)

    for _, expected_path in enumerate(expected_paths):
        assert expected_path in baked_files_no_pycache


def test_with_default_configuration(
    cookies: Cookies, default_context: typing.Dict[str, str]
) -> None:
    baked_project = cookies.bake(extra_context=default_context)

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

    check_paths_exist(
        get_expected_baked_default_files(default_context['package_name']),
        rel_baked_files,
    )


def test_with_parameterized_configuration(  # noqa: C901
    cookies: Cookies, context: typing.Dict[str, str]
) -> None:

    if not bool(strtobool(context['should_install_github_dependabot'])):
        context['should_automerge_autoapprove_github_dependabot'] = 'n'

    if not bool(strtobool(context['should_install_github_actions'])):
        context['should_automerge_autoapprove_github_dependabot'] = 'n'

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

    print(f"author file: {context['should_create_author_files']}")
    print(f"dependabot: {context['should_install_github_dependabot']}")
    print(
        f"automerge_autoapprove_dependabot: {context['should_automerge_autoapprove_github_dependabot']}"  # noqa: B950
    )
    print(f"gh actions: {context['should_install_github_actions']}")
    print(f"pypi: {context['should_publish_to_pypi']}")

    if (
        strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and strtobool(context['should_publish_to_pypi'])
    ):
        if strtobool(
            context['should_automerge_autoapprove_github_dependabot']
        ):  # noqa: B950
            check_paths_exist(
                get_expected_baked_default_files(context['package_name']),
                rel_baked_files,
            )
        else:
            check_paths_exist(
                list(
                    set(
                        get_expected_baked_default_files(
                            context['package_name']
                        )
                    )
                    - set(
                        EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
                    )
                ),  # noqa: B950
                rel_baked_files,
            )
    elif (
        strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and not strtobool(context['should_publish_to_pypi'])
    ):
        if strtobool(
            context['should_automerge_autoapprove_github_dependabot']
        ):  # noqa: B950
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
                + EXPECTED_BAKED_AUTHORS_FILES
                + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
                rel_baked_files,
            )
        else:
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
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
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES,
            rel_baked_files,
        )
    elif (
        strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and strtobool(context['should_publish_to_pypi'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES,
            rel_baked_files,
        )
    elif (
        strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and not strtobool(context['should_publish_to_pypi'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_AUTHORS_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and not strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_AUTHORS_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and strtobool(context['should_publish_to_pypi'])
    ):
        if strtobool(
            context['should_automerge_autoapprove_github_dependabot']
        ):  # noqa: B950
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
                + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES,
                rel_baked_files,
            )
        else:
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
                + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES,
                rel_baked_files,
            )
    elif (
        not strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and not strtobool(context['should_publish_to_pypi'])
    ):
        if strtobool(
            context['should_automerge_autoapprove_github_dependabot']
        ):  # noqa: B950
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
                + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_AUTOAPPROVE_AUTOMERGE_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
                rel_baked_files,
            )
        else:
            check_paths_exist(
                get_expected_baked_files(context['package_name'])
                + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES
                + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
                rel_baked_files,
            )
    elif (
        not strtobool(context['should_create_author_files'])
        and strtobool(context['should_install_github_dependabot'])
        and not strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_GITHUB_DEPENDABOT_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and strtobool(context['should_publish_to_pypi'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES
            + EXPECTED_BAKED_GITHUB_ACTIONS_PYPI_PUBLISH_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and strtobool(context['should_install_github_actions'])
        and not strtobool(context['should_publish_to_pypi'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name'])
            + EXPECTED_BAKED_GITHUB_ACTIONS_FILES,
            rel_baked_files,
        )
    elif (
        not strtobool(context['should_create_author_files'])
        and not strtobool(context['should_install_github_dependabot'])
        and not strtobool(context['should_install_github_actions'])
    ):
        check_paths_exist(
            get_expected_baked_files(context['package_name']), rel_baked_files
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
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'ci.yml' in path:
            with open(path, 'rb', 0) as file, mmap.mmap(
                file.fileno(), 0, access=mmap.ACCESS_READ
            ) as s:
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
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'Dockerfile' in path:
            with open(path, 'rb', 0) as file, mmap.mmap(
                file.fileno(), 0, access=mmap.ACCESS_READ
            ) as s:
                if s.find(f"POETRY_VERSION={poetry_version}".encode()) == -1:
                    pytest.fail('Should have appropriate poetry version')


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
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'pyproject.toml' in path:
            with open(path, 'rb', 0) as file, mmap.mmap(
                file.fileno(), 0, access=mmap.ACCESS_READ
            ) as s:
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
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'pyproject.toml' in path:
            with open(path, 'rb', 0) as file, mmap.mmap(
                file.fileno(), 0, access=mmap.ACCESS_READ
            ) as s:
                if s.find(b'[tool.mypy]') == -1:
                    pytest.fail('Should have mypy configuration section')


# vim: fenc=utf-8
# vim: filetype=python
