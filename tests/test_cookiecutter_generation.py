"""
Tests project generation
"""

import os
import re

from typing import List

from binaryornot.check import is_binary
import pytest


PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


EXPECTED_BAKED_PROJECT_FILES = [
    '.commitlint.config.js',
    '.coveragerc',
    '.dockerignore',
    '.flake8',
    '.github/dependabot.yml',
    '.github/labeler.yml',
    '.github/workflows/ci.yml',
    '.github/workflows/codeql-analysis.yml',
    '.github/workflows/commitlint.yml',
    '.github/workflows/hadolint.yml',
    '.github/workflows/pr-labeler.yml',
    '.github/workflows/pr-size-labeler.yml',
    '.gitignore',
    '.konchrc',
    '.pre-commit-config.yaml',
    'AUTHORS.rst',
    'Dockerfile',
    'HISTORY.rst',
    'LICENSE',
    'Makefile',
    'README.rst',
    'docs/Makefile',
    'docs/conf.py',
    'docs/index.rst',
    'docs/make.bat',
    'logging.yaml',
    'pyproject.toml',
    'pytest.ini',
    'setup.cfg',
    'test_project/__init__.py',
    'test_project/test_project.py',
    'tests/test_test_project.py',
    'tox.ini',
]


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
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
    for i, baked_file in enumerate(baked_files):
        assert expected_paths[i] in baked_file


def test_with_default_configuration(cookies, context):

    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path.is_dir()

    baked_files = build_files_list(str(baked_project.project_path))
    baked_files.sort()

    assert baked_files

    check_paths_substitution(baked_files)
    check_paths_exist(EXPECTED_BAKED_PROJECT_FILES, baked_files)
