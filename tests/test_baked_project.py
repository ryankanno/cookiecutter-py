#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Runs a generated project end to end."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest
from pytest_cookies.plugin import Cookies


# tox exports these for *this* project. Left set, uv would sync the baked
# project into this repo's environment rather than its own.
INHERITED_ENV_VARS = ('VIRTUAL_ENV', 'UV_PROJECT_ENVIRONMENT')

TIMEOUT_SECONDS = 900

HADOLINT_IMAGE = 'hadolint/hadolint:latest'
IMAGE_TAG = 'cookiecutter-py-baked:test'


def run(
    command: list[str], cwd: Path, check: bool = True
) -> subprocess.CompletedProcess[str]:
    executable = shutil.which(command[0])
    assert executable is not None, f'{command[0]} is not installed'

    env = {
        key: value
        for key, value in os.environ.items()
        if key not in INHERITED_ENV_VARS
    }

    result = subprocess.run(
        [executable, *command[1:]],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )

    if check and result.returncode != 0:
        pytest.fail(
            f'{" ".join(command)} failed in {cwd}\n'
            f'stdout:\n{result.stdout}\n'
            f'stderr:\n{result.stderr}'
        )

    return result


@pytest.mark.bake
def test_baked_project_runs(
    cookies: Cookies, default_context: dict[str, str]
) -> None:
    baked_project = cookies.bake(extra_context=default_context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path

    project = Path(baked_project.project_path)

    # The bootstrap the generated README documents. Creates uv.lock.
    run(['uv', 'sync'], cwd=project)

    # Every tox env in the generated project runs this, so a missing or
    # inconsistent lock breaks that project's own CI before it starts.
    run(['uv', 'sync', '--locked'], cwd=project)

    run(['uv', 'run', 'pytest'], cwd=project)
    run(['uv', 'run', 'ruff', 'check', '.'], cwd=project)


@pytest.mark.docker
def test_baked_project_docker_image(cookies: Cookies) -> None:
    # Baked with the real cookiecutter.json defaults, not default_context,
    # which carries placeholder versions like uv_version "0.0.1" that do
    # not resolve as image tags.
    baked_project = cookies.bake()

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path

    project = Path(baked_project.project_path)

    # The Dockerfile does `COPY uv.lock`, which does not exist until the
    # documented bootstrap has run.
    run(['uv', 'lock'], cwd=project)

    # hadolint cannot parse the template itself, only a rendered Dockerfile,
    # so this is the earliest point it can run at all.
    run(
        [
            'docker',
            'run',
            '--rm',
            '--volume',
            f'{project}:/workspace',
            '--workdir',
            '/workspace',
            HADOLINT_IMAGE,
            'hadolint',
            'Dockerfile',
        ],
        cwd=project,
    )

    run(['docker', 'build', '--tag', IMAGE_TAG, '.'], cwd=project)

    try:
        result = run(
            ['docker', 'run', '--rm', '--entrypoint', 'id', IMAGE_TAG],
            cwd=project,
        )
        # The final stage must not run as root. This is what DL3066 and the
        # generated project's hadolint workflow are guarding.
        assert 'uid=0(root)' not in result.stdout, (
            f'image should not run as root, got: {result.stdout.strip()}'
        )
    finally:
        run(['docker', 'rmi', '--force', IMAGE_TAG], cwd=project, check=False)


# vim: fenc=utf-8
# vim: filetype=python
