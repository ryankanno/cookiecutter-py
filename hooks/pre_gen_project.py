#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import sys
from distutils.util import strtobool


VALID_PYTHON_VERSION_PREFIXES = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "pypy3.9",
    "pypy3.10",
]


def validate_supported_python_versions(supported_python_versions: str) -> None:
    supported_python_versions_list = [
        py_version.strip()
        for py_version in supported_python_versions.split(',')
    ]

    for version in supported_python_versions_list:
        if not version.startswith(tuple(VALID_PYTHON_VERSION_PREFIXES)):
            print(
                f"ERROR: {version} is not a valid supported Python version. "
                f"Supported are any Pythons that begin with the following prefixes: {VALID_PYTHON_VERSION_PREFIXES}"  # noqa: B950
            )
            sys.exit(1)


def validate_dependabot(
    should_install_dependabot: bool,
    should_install_automerge: bool,
    should_install_gh_actions: bool,
) -> None:
    if not should_install_dependabot and should_install_automerge:
        print(
            "ERROR: You must install dependabot if you want to install the automerge workflow."  # noqa: B950
        )
        sys.exit(1)
    elif not should_install_gh_actions and should_install_automerge:
        print(
            "ERROR: You must install Github Actions if you want to install the Dependabot automerge workflow."  # noqa: B950
        )
        sys.exit(1)


if __name__ == '__main__':
    validate_supported_python_versions(
        '{{ cookiecutter.supported_python_versions }}'
    )
    validate_dependabot(
        bool(strtobool('{{ cookiecutter.should_install_github_dependabot }}')),
        bool(
            strtobool(
                '{{ cookiecutter.should_automerge_autoapprove_github_dependabot }}'
            )
        ),  # noqa: B950
        bool(strtobool('{{ cookiecutter.should_install_github_actions }}')),
    )


# vim: fenc=utf-8
# vim: filetype=python
