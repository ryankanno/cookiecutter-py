#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Tests for strtobool utility function in both hooks."""

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

# Add hooks directory to path to import from hook files
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from post_gen_project import strtobool as post_gen_strtobool  # noqa: E402
from pre_gen_project import strtobool as pre_gen_strtobool  # noqa: E402


class TestStrtobool:
    """Test strtobool function in both hooks."""

    @staticmethod
    @pytest.mark.parametrize(
        'strtobool_func',
        [post_gen_strtobool, pre_gen_strtobool],
        ids=['post_gen_project', 'pre_gen_project'],
    )
    @pytest.mark.parametrize(
        'value',
        ['y', 'yes', 't', 'true', 'on', '1', 'Y', 'YES', 'True', 'ON'],
    )
    def test_true_values(
        strtobool_func: Callable[[str], int], value: str
    ) -> None:
        """Test that true values return 1."""
        assert strtobool_func(value) == 1

    @staticmethod
    @pytest.mark.parametrize(
        'strtobool_func',
        [post_gen_strtobool, pre_gen_strtobool],
        ids=['post_gen_project', 'pre_gen_project'],
    )
    @pytest.mark.parametrize(
        'value',
        ['n', 'no', 'f', 'false', 'off', '0', 'N', 'NO', 'False', 'OFF'],
    )
    def test_false_values(
        strtobool_func: Callable[[str], int], value: str
    ) -> None:
        """Test that false values return 0."""
        assert strtobool_func(value) == 0

    @staticmethod
    @pytest.mark.parametrize(
        'strtobool_func',
        [post_gen_strtobool, pre_gen_strtobool],
        ids=['post_gen_project', 'pre_gen_project'],
    )
    @pytest.mark.parametrize('value', ['invalid', 'maybe', '2', '', 'yesno'])
    def test_invalid_values(
        strtobool_func: Callable[[str], int], value: str
    ) -> None:
        """Test that invalid values raise ValueError."""
        with pytest.raises(ValueError, match="invalid truth value"):
            strtobool_func(value)


# vim: fenc=utf-8
# vim: filetype=python
