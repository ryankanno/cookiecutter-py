#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import sys


VALID_PYTHON_VERSION_PREFIXES = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "pypy3.7",
    "pypy3.8",
    "pypy3.9",
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


if __name__ == '__main__':
    validate_supported_python_versions(
        '{{ cookiecutter.supported_python_versions }}'
    )


# vim: fenc=utf-8
# vim: filetype=python
