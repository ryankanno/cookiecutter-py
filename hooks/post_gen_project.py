#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from pathlib import Path
from distutils.util import strtobool


PROJECT_ROOT_DIR = Path.cwd().absolute()
PROJECT_GITHUB = PROJECT_ROOT_DIR / Path(".github")


def remove_path(path: Path) -> None:
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        remove_path(p)
    path.rmdir()


def manage_author_files(should_create_author_files: str) -> None:
    if not strtobool(should_create_author_files):
        remove_path(PROJECT_ROOT_DIR / Path("AUTHORS.rst"))


def manage_github_files(
    should_install_github_dependabot: str, should_install_github_actions: str
) -> None:

    if not strtobool(should_install_github_dependabot):
        remove_path(PROJECT_GITHUB / Path("dependabot.yml"))

    if not strtobool(should_install_github_actions):
        remove_path(PROJECT_GITHUB / Path("labeler.yml"))
        remove_path(PROJECT_GITHUB / Path("release-drafter.yml"))
        remove_path(PROJECT_GITHUB / Path("workflows"))

    if not any(Path(PROJECT_GITHUB).iterdir()):
        remove_path(PROJECT_GITHUB)


if __name__ == '__main__':
    manage_author_files('{{ cookiecutter.should_create_author_files }}')
    manage_github_files(
        '{{ cookiecutter.should_install_github_dependabot }}',
        '{{ cookiecutter.should_install_github_actions}}',
    )


# vim: fenc=utf-8
# vim: filetype=python
