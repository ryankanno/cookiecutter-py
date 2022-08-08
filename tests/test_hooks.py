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


def test_remove_path() -> None:
    temp = tempfile.NamedTemporaryFile(delete=False)
    remove_path(Path(temp.name))

    assert not os.path.exists(temp.name)


# vim: fenc=utf-8
# vim: filetype=python
