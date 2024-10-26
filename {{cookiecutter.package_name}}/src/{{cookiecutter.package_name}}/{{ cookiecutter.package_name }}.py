#!/usr/bin/env python
#
# Copyright © , {% now 'utc', '%Y' %}, {{cookiecutter.author_name }} <{{ cookiecutter.author_email }}>  # noqa: B950, E501
#
# Distributed under terms of the MIT license.

"""Default module for {{ cookiecutter.package_name }}."""

import structlog


LOGGER = structlog.get_logger(__name__)


def hello_world() -> str:
    return "Hello World"


if __name__ == "__main__":
    print(hello_world())  # noqa: T201


# vim: fenc=utf-8
# vim: filetype=python
