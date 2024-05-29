#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import fileinput
from distutils.util import strtobool
from pathlib import Path


PROJECT_ROOT_DIR = Path.cwd().absolute()
PROJECT_GITHUB = PROJECT_ROOT_DIR / Path(".github")


def remove_path(path: Path) -> None:
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    if path.exists():
        for p in path.iterdir():
            remove_path(p)
        path.rmdir()


def manage_direnv_files(should_use_direnv: str) -> None:
    if not strtobool(should_use_direnv):
        remove_path(PROJECT_ROOT_DIR / Path(".envrc"))


def manage_author_files(should_create_author_files: str) -> None:
    if not strtobool(should_create_author_files):
        remove_path(PROJECT_ROOT_DIR / Path("AUTHORS.rst"))


def manage_github_files(
    should_install_github_dependabot: str,
    should_automerge_autoapprove_github_dependabot: str,
    should_install_github_actions: str,
    should_publish_to_pypi: str,
) -> None:
    if not strtobool(should_install_github_dependabot):
        remove_path(PROJECT_GITHUB / Path("dependabot.yml"))
        remove_path(
            PROJECT_GITHUB
            / Path("workflows")
            / Path("auto-approve-merge-dependabot.yml")
        )

    if not strtobool(
        should_automerge_autoapprove_github_dependabot
    ) and strtobool(should_install_github_dependabot):
        remove_path(
            PROJECT_GITHUB
            / Path("workflows")
            / Path("auto-approve-merge-dependabot.yml")
        )

    if not strtobool(should_install_github_actions):
        remove_path(PROJECT_GITHUB / Path("labeler.yml"))
        remove_path(PROJECT_GITHUB / Path("release-drafter.yml"))
        remove_path(PROJECT_GITHUB / Path("workflows"))
    elif not strtobool(should_publish_to_pypi):
        remove_path(PROJECT_GITHUB / Path("workflows") / Path("publish.yml"))

    if not any(Path(PROJECT_GITHUB).iterdir()):
        remove_path(PROJECT_GITHUB)


def update_pyproject_version(
    version: str,
) -> None:
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.is_file():
        with pyproject_path.open() as f:
            pyproject = f.read()
        pyproject = pyproject.replace(
            'version = "0.0.0"', f"version = {version!r}"
        )
        with pyproject_path.open("w") as f:
            f.write(pyproject)


def uncomment_pyproject_python_dependency() -> None:
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.is_file():
        with fileinput.input(pyproject_path, inplace=True) as file:
            for line in file:
                if line.strip().startswith('# python'):
                    new_line = line.replace('# python', 'python')
                    print(new_line, end='')  # noqa: T201
                else:
                    print(line, end='')  # noqa: T201


if __name__ == '__main__':
    manage_direnv_files('{{ cookiecutter.should_use_direnv }}')
    manage_author_files('{{ cookiecutter.should_create_author_files }}')
    manage_github_files(
        '{{ cookiecutter.should_install_github_dependabot }}',
        '{{ cookiecutter.should_automerge_autoapprove_github_dependabot }}',
        '{{ cookiecutter.should_install_github_actions}}',
        '{{ cookiecutter.should_publish_to_pypi }}',
    )
    update_pyproject_version('{{ cookiecutter.version  }}')
    uncomment_pyproject_python_dependency()


# vim: fenc=utf-8
# vim: filetype=python
