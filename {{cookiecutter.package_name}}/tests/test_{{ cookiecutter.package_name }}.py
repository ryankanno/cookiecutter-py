#!/usr/bin/env python
#
# flake8: noqa

"""
Tests for `{{ cookiecutter.package_name }}` package.
"""

# fmt: off

from {{cookiecutter.package_name}} import {{ cookiecutter.package_name }}


# fmt: on


def test_hello_world() -> None:
    assert {{ cookiecutter.package_name }}.hello_world() == "Hello World"


# vim: filetype=python
