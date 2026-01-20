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
import sys
from pathlib import Path

import pytest
from binaryornot.check import is_binary
from pytest_cookies.plugin import Cookies

# Add hooks directory to path to import from hook files
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from pre_gen_project import strtobool  # noqa: E402

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


def get_expected_baked_files(package_name: str) -> list[str]:
    return EXPECTED_BASE_BAKED_FILES + [
        f'/src/{package_name}/__init__.py',
        f'/src/{package_name}/{package_name}.py',
        '/tests/__init__.py',
        f'/tests/test_{package_name}.py',
    ]


def build_files_list(root_dir: str, is_absolute: bool = True) -> list[str]:
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


def check_paths_substitution(paths: list[str]) -> None:
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
    expected_paths: list[str], baked_files: list[str]
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
    cookies: Cookies, default_context: dict[str, str]
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
    cookies: Cookies, context: dict[str, str]
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

    # publish.yml always exists when GitHub Actions is enabled
    # Individual publish jobs are conditionally included via Jinja2
    if strtobool(context['should_install_github_actions']):
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
    cookies: Cookies, default_context: dict[str, str], codecov: str
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


@pytest.mark.parametrize('publish_testpypi', ['y', 'n'])
def test_with_publish_to_testpypi(
    cookies: Cookies, default_context: dict[str, str], publish_testpypi: str
) -> None:
    default_context['should_publish_to_testpypi'] = publish_testpypi
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'publish.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if (
                    s.find(b'publish_test_pypi:') == -1
                    and publish_testpypi == 'y'
                ):
                    pytest.fail('Should have publish_test_pypi job')
                elif (
                    s.find(b'publish_test_pypi:') != -1
                    and publish_testpypi == 'n'
                ):
                    pytest.fail('Should not have publish_test_pypi job')


@pytest.mark.parametrize('publish_github_packages', ['y', 'n'])
def test_with_publish_to_github_packages(
    cookies: Cookies,
    default_context: dict[str, str],
    publish_github_packages: str,
) -> None:
    default_context['should_publish_to_github_packages'] = (
        publish_github_packages
    )
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'publish.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if (
                    s.find(b'publish_github_packages:') == -1
                    and publish_github_packages == 'y'
                ):
                    pytest.fail('Should have publish_github_packages job')
                elif (
                    s.find(b'publish_github_packages:') != -1
                    and publish_github_packages == 'n'
                ):
                    pytest.fail('Should not have publish_github_packages job')


@pytest.mark.parametrize('attach_release', ['y', 'n'])
def test_with_attach_to_github_release(
    cookies: Cookies, default_context: dict[str, str], attach_release: str
) -> None:
    default_context['should_attach_to_github_release'] = attach_release
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'publish.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if (
                    s.find(b'attach_to_release:') == -1
                    and attach_release == 'y'
                ):
                    pytest.fail('Should have attach_to_release job')
                elif (
                    s.find(b'attach_to_release:') != -1
                    and attach_release == 'n'
                ):
                    pytest.fail('Should not have attach_to_release job')


@pytest.mark.parametrize(
    (
        'testpypi',
        'pypi',
        'github_packages',
        'attach_release',
        'expected_job_count',
    ),
    [
        # All disabled - file should STILL exist (with only build job)
        ('n', 'n', 'n', 'n', 1),
        # Only TestPyPI enabled
        ('y', 'n', 'n', 'n', 2),
        # Only PyPI enabled
        ('n', 'y', 'n', 'n', 2),
        # Only GitHub Packages enabled
        ('n', 'n', 'y', 'n', 2),
        # Only attach to release enabled
        ('n', 'n', 'n', 'y', 2),
        # All enabled
        ('y', 'y', 'y', 'y', 5),
    ],
)
def test_publish_yml_always_exists_with_github_actions(
    cookies: Cookies,
    default_context: dict[str, str],
    testpypi: str,
    pypi: str,
    github_packages: str,
    attach_release: str,
    expected_job_count: int,
) -> None:
    default_context['should_publish_to_testpypi'] = testpypi
    default_context['should_publish_to_pypi'] = pypi
    default_context['should_publish_to_github_packages'] = github_packages
    default_context['should_attach_to_github_release'] = attach_release
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    rel_baked_files = build_files_list(
        str(baked_project.project_path), is_absolute=False
    )

    publish_yml_path = '/.github/workflows/publish.yml'
    if publish_yml_path not in rel_baked_files:
        pytest.fail(
            'publish.yml should always exist when GitHub Actions is enabled'
        )

    # Count jobs in the workflow file
    abs_baked_files = build_files_list(str(baked_project.project_path))
    for path in abs_baked_files:
        if 'publish.yml' in path:
            with Path(path).open('r') as file:
                content = file.read()
                # Count job definitions (lines that match pattern "  job_name:")
                # Jobs are defined at the top level under "jobs:" with 2-space indent
                job_count = 0
                in_jobs_section = False
                for line in content.split('\n'):
                    stripped = line.strip()
                    # Track when we enter the jobs section
                    if stripped == 'jobs:':
                        in_jobs_section = True
                        continue
                    # If we're in jobs section and hit a top-level key, we're out
                    if in_jobs_section and line and not line.startswith(' '):
                        in_jobs_section = False
                    # Count jobs only within jobs section
                    if (
                        in_jobs_section
                        and line.startswith('  ')
                        and ':' in line
                        and not line.startswith('    ')
                    ):
                        # Check it's a job definition, not a property within a job
                        if (
                            stripped
                            and not stripped.startswith('#')
                            and stripped.endswith(':')
                        ):
                            job_count += 1

                if job_count != expected_job_count:
                    pytest.fail(
                        f'Expected {expected_job_count} jobs, found {job_count}'
                    )


@pytest.mark.parametrize('testpypi_enabled', ['y', 'n'])
def test_publish_pypi_job_dependencies(
    cookies: Cookies, default_context: dict[str, str], testpypi_enabled: str
) -> None:
    default_context['should_publish_to_testpypi'] = testpypi_enabled
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if 'publish.yml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                # Look for the publish_pypi job and its needs line
                content = s.read().decode('utf-8')
                if 'publish_pypi:' in content:
                    if testpypi_enabled == 'y':
                        # Should have both build and publish_test_pypi as dependencies
                        if 'needs: [build, publish_test_pypi]' not in content:
                            pytest.fail(
                                'publish_pypi should depend on [build, publish_test_pypi] when TestPyPI is enabled'
                            )
                    else:
                        # Should only have build as dependency
                        if 'needs: [build, publish_test_pypi]' in content:
                            pytest.fail(
                                'publish_pypi should not depend on publish_test_pypi when TestPyPI is disabled'
                            )
                        if 'needs: [build]' not in content:
                            pytest.fail(
                                'publish_pypi should depend on [build] when TestPyPI is disabled'
                            )


@pytest.mark.parametrize('uv_version', ['8.0.8', '4.2.0'])
def test_with_uv_version(
    cookies: Cookies,
    default_context: dict[str, str],
    uv_version: str,
) -> None:
    default_context['uv_version'] = uv_version
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
                if s.find(f"UV_VERSION={uv_version}".encode()) == -1:
                    pytest.fail('Should have appropriate uv version')


@pytest.mark.parametrize('tox_version', ['8.0.8', '4.2.0'])
def test_with_tox_version(
    cookies: Cookies,
    default_context: dict[str, str],
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
                if s.find(f"TOX_VERSION: {tox_version}".encode()) == -1:
                    pytest.fail('Should have appropriate tox version')


@pytest.mark.parametrize('version', ['42.0', '4.2.0'])
def test_with_version(
    cookies: Cookies,
    default_context: dict[str, str],
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


def test_justfile_lint_command_structure(
    cookies: Cookies,
    default_context: dict[str, str],
) -> None:
    """Verify the generated Justfile has the correct lint command structure.

    The lint recipe should:
    - Accept variable arguments (*LINT_ARGS)
    - Check if --fix is passed and route to lint-fix tox environment
    - Otherwise run the lint tox environment
    - Not have a standalone lint-fix recipe
    """
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    for path in abs_baked_files:
        if path.endswith('Justfile'):
            with Path(path).open('rb', 0) as file:
                content = file.read()

                # Check that lint recipe accepts arguments
                if b'lint *LINT_ARGS:' not in content:
                    msg = 'Justfile should have lint recipe with '
                    msg += '*LINT_ARGS parameter'
                    pytest.fail(msg)

                # Check that lint recipe has conditional logic for --fix
                if b'if [[ "{{LINT_ARGS}}" == "--fix" ]]' not in content:
                    pytest.fail(
                        'Justfile lint recipe should check for --fix flag'
                    )

                # Check that it calls lint-fix tox environment
                # when --fix is passed
                if b'just tox run -e lint-fix' not in content:
                    msg = 'Justfile should call tox lint-fix '
                    msg += 'environment when --fix is passed'
                    pytest.fail(msg)

                # Check that it calls lint tox environment by default
                if b'just tox run -e lint {{LINT_ARGS}}' not in content:
                    pytest.fail(
                        'Justfile should call tox lint environment by default'
                    )

                # Ensure there's no standalone lint-fix recipe
                # Look for pattern indicating a separate recipe definition
                lines = content.decode('utf-8').split('\n')
                for line in lines:
                    # Check for standalone lint-fix recipe
                    # (not inside lint recipe)
                    if not line.startswith('lint-fix'):
                        continue
                    # Make sure it's not commented out
                    stripped = line.strip()
                    if stripped.startswith('#'):
                        continue
                    msg = 'Justfile should not have a '
                    msg += 'standalone lint-fix recipe'
                    pytest.fail(msg)


def test_pyproject_with_default_configuration(
    cookies: Cookies,
    default_context: dict[str, str],
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


@pytest.mark.parametrize('python_version', ['3.10', '3.11', '3.12', '3.13'])
def test_with_python_version(
    cookies: Cookies,
    default_context: dict[str, str],
    python_version: str,
) -> None:
    """Verify generated project supports specified Python version."""
    default_context['python_version'] = python_version
    default_context['supported_python_versions'] = (
        "3.10, 3.11, 3.12, 3.13, pypy3.10, pypy3.11"
    )

    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path
    assert baked_project.project_path.is_dir()

    abs_baked_files = build_files_list(str(baked_project.project_path))

    # Verify python version appears in generated pyproject.toml
    for path in abs_baked_files:
        if 'pyproject.toml' in path:
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                if (
                    s.find(
                        f"requires-python = \">={python_version}\"".encode()
                    )
                    == -1
                ):
                    pytest.fail(
                        f'pyproject.toml requires Python {python_version}'
                    )

    # Verify tox.ini includes python version environments
    for path in abs_baked_files:
        if path.endswith('tox.ini'):
            with (
                Path(path).open('rb', 0) as file,
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s,
            ):
                py_env = f"py{python_version.replace('.', '')}".encode()
                if s.find(py_env) == -1:
                    pytest.fail(
                        f'tox.ini should include {py_env.decode()} environment'
                    )


# vim: fenc=utf-8
# vim: filetype=python
