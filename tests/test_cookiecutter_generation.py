"""
Tests project generation
"""

import os
import re

import pytest


def test_with_default_configuration(cookies, context):

    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path.is_dir()
