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

    def test_something(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass

# vim: filetype=python
