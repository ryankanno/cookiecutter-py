#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `{{ cookiecutter.module_name }}` module.
"""

from {{ cookiecutter.module_name }} import {{ cookiecutter.module_name }}


class Test{{ cookiecutter.repo_name|capitalize }}(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_hello_world(self):
        assert {{ cookiecutter.module_name }}.hello_world() == "Hello World"

    @classmethod
    def teardown_class(cls):
        pass

# vim: filetype=python
