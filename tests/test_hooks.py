#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""
Tests hooks
"""

import os
from pathlib import Path
import tempfile

import pytest

from hooks.post_gen_project import remove_path
from hooks.pre_gen_project import validate_supported_python_versions


def test_remove_path() -> None:
    temp = tempfile.NamedTemporaryFile(delete=False)
    remove_path(Path(temp.name))

    assert not os.path.exists(temp.name)


def test_with_unsupported_python_versions() -> None:
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_supported_python_versions("foo")

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_with_supported_python_versions() -> None:
    validate_supported_python_versions(
        "3.7, 3.8, 3.9, 3.10, 3.11, pypy3.7, pypy3.8, pypy3.9"
    )  # noqa: B950


# vim: fenc=utf-8
# vim: filetype=python
