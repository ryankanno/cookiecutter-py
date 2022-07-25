#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# flake8: noqa

"""
Tests for `{{ cookiecutter.package_name }}` package.
"""

from {{ cookiecutter.package_name }} import {{ cookiecutter.package_name }}


class Test{{ cookiecutter.project_name|replace(' ', '')}}(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_hello_world(self):
        assert {{ cookiecutter.package_name }}.hello_world() == "Hello World"

    @classmethod
    def teardown_class(cls):
        pass

# vim: filetype=python
