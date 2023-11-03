#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""
Tests hooks
"""

import os
import tempfile
from pathlib import Path

import pytest

from hooks.post_gen_project import remove_path
from hooks.pre_gen_project import (
    validate_dependabot,
    validate_supported_python_versions,
)


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
        "3.9, 3.10, 3.11, 3.12, pypy3.9, pypy3.10",
    )  # noqa: B950


def test_with_invalid_dependabot_settings() -> None:
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, True)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, False)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(True, True, False)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, False)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_with_valid_dependabot_settings() -> None:
    validate_dependabot(True, True, True)
    validate_dependabot(True, False, True)
    validate_dependabot(True, False, False)
    validate_dependabot(False, False, False)


# vim: fenc=utf-8
# vim: filetype=python
