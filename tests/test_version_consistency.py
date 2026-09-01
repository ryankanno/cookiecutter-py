#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Tests that tool versions agree across the places they are declared.

Several tools are pinned in more than one file, and nothing else checks
they match. Every mismatch these tests describe has happened at least
once: uv ran at a different version locally than in CI, ruff was five
minor versions behind its own hook, and the template kept 2024 pins while
this repo moved on.
"""

import json
import re
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_ROOT = REPO_ROOT / '{{cookiecutter.package_name}}'

# `- repo: <url>` followed by `rev: <value>`, which is enough structure to
# read a pre-commit config without taking on a YAML dependency.
HOOK_REV = re.compile(
    r'-\s+repo:\s*(?P<repo>\S+)\s*\n\s*rev:\s*"?(?P<rev>[^"\s]+)"?'
)

ENV_VERSION = re.compile(
    r'^\s*(?P<name>UV_VERSION|TOX_VERSION):\s*(?P<value>\S+)',
    re.MULTILINE,
)

# Hook repository -> the package it installs, so a rev can be compared
# against what uv resolves.
HOOK_PACKAGES = {
    'https://github.com/astral-sh/uv-pre-commit': 'uv',
    'https://github.com/astral-sh/ruff-pre-commit': 'ruff',
    'https://github.com/pre-commit/mirrors-mypy': 'mypy',
    'https://github.com/fpgmaas/deptry.git': 'deptry',
}


def locked_versions() -> dict[str, str]:
    """Every package version uv resolved, by name."""
    lock = tomllib.loads((REPO_ROOT / 'uv.lock').read_text(encoding='utf-8'))
    return {p['name']: p['version'] for p in lock['package']}


def hook_revs(config: Path) -> dict[str, str]:
    """Hook revisions by repository url, with any leading `v` stripped."""
    text = config.read_text(encoding='utf-8')
    return {
        match['repo']: match['rev'].lstrip('v')
        for match in HOOK_REV.finditer(text)
    }


def workflow_env_versions(name: str) -> dict[str, str]:
    """Declared value of `name` in each workflow that uses it.

    Keyed by filename rather than collapsed into a set, so that a workflow
    which references the variable without declaring it is visible. Such a
    workflow expands `${{ env.NAME }}` to an empty string and silently
    installs an unpinned tool, which is the drift these tests exist to
    catch — but it would not change the set of declared values.
    """
    usage = re.compile(r'\$\{\{\s*env\.' + name + r'\s*\}\}')
    declaration = re.compile(
        r'^\s*' + name + r':\s*(?P<value>\S+)', re.MULTILINE
    )

    found: dict[str, str] = {}
    for workflow in (REPO_ROOT / '.github' / 'workflows').glob('*.yml'):
        text = workflow.read_text(encoding='utf-8')
        if not usage.search(text):
            continue
        match = declaration.search(text)
        found[workflow.name] = match['value'] if match else '<undeclared>'
    return found


def test_hook_revs_match_the_lockfile() -> None:
    """Each pinned hook runs the version uv resolved.

    When these differ, `just lint` and `pre-commit` lint with different
    binaries, which has produced "All checks passed" from one and six
    errors from the other.
    """
    locked = locked_versions()
    revs = hook_revs(REPO_ROOT / '.pre-commit-config.yaml')

    mismatches = [
        f'{package}: hook pins {rev}, uv.lock resolves {locked[package]}'
        for repo, package in HOOK_PACKAGES.items()
        if (rev := revs.get(repo)) is not None
        and package in locked
        and rev != locked[package]
    ]

    assert not mismatches, 'hook and lockfile disagree:\n' + '\n'.join(
        mismatches
    )


def test_uv_version_agrees_everywhere() -> None:
    """Five places pin uv, and they must agree.

    The lockfile, a pre-commit hook, three workflow env blocks and the
    template default. Nothing propagates between them.
    """
    locked = locked_versions()['uv']
    envs = workflow_env_versions('UV_VERSION')
    hook = hook_revs(REPO_ROOT / '.pre-commit-config.yaml')[
        'https://github.com/astral-sh/uv-pre-commit'
    ]
    template_default = json.loads(
        (REPO_ROOT / 'cookiecutter.json').read_text(encoding='utf-8')
    )['uv_version']

    assert envs, 'no workflow references UV_VERSION; has it been renamed?'

    declared = {
        'uv.lock': locked,
        'pre-commit rev': hook,
        'cookiecutter.json': template_default,
        **{f'workflow {name}': value for name, value in envs.items()},
    }

    assert len(set(declared.values())) == 1, (
        'uv version differs across declarations:\n'
        + '\n'.join(f'  {k}: {v}' for k, v in declared.items())
    )


def test_tox_version_agrees_everywhere() -> None:
    """Four places pin tox, and they must agree.

    The lockfile, two workflow env blocks and the template default. CI
    installs the pinned version, so a drifted lockfile means local and CI
    run different tox.
    """
    locked = locked_versions()['tox']
    envs = workflow_env_versions('TOX_VERSION')
    template_default = json.loads(
        (REPO_ROOT / 'cookiecutter.json').read_text(encoding='utf-8')
    )['tox_version']

    assert envs, 'no workflow references TOX_VERSION; has it been renamed?'

    declared = {
        'uv.lock': locked,
        'cookiecutter.json': template_default,
        **{f'workflow {name}': value for name, value in envs.items()},
    }

    assert len(set(declared.values())) == 1, (
        'tox version differs across declarations:\n'
        + '\n'.join(f'  {k}: {v}' for k, v in declared.items())
    )


def test_template_hook_revs_match_this_repo() -> None:
    """The template pins the same hook versions this repo uses.

    Generated projects should lint with the same tools as the repo that
    generates them, or the template's own reference code can pass here and
    fail there.
    """
    ours = hook_revs(REPO_ROOT / '.pre-commit-config.yaml')
    theirs = hook_revs(TEMPLATE_ROOT / '.pre-commit-config.yaml')

    mismatches = [
        f'{repo.rsplit("/", 1)[-1]}: template {rev}, this repo {ours[repo]}'
        for repo, rev in theirs.items()
        if repo in ours and not rev.startswith('{{') and rev != ours[repo]
    ]

    assert not mismatches, (
        'template and repo hook revs disagree:\n' + '\n'.join(mismatches)
    )


# vim: fenc=utf-8
# vim: filetype=python
