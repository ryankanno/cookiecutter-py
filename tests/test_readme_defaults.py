#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Tests that README defaults match cookiecutter.json."""

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent

# Matches "- `option_name` - description (default: value)" in the README's
# template options list.
DOCUMENTED_DEFAULT = re.compile(
    r'`(?P<option>[a-z_]+)` - [^(\n]*\(default: (?P<value>[^)]+)\)'
)


def test_readme_documents_the_real_defaults() -> None:
    """Every default stated in the README matches cookiecutter.json.

    The README restates values that live in cookiecutter.json, so changing
    a default silently invalidates the prose. Three had drifted before this
    test existed.
    """
    cookiecutter = json.loads(
        (REPO_ROOT / 'cookiecutter.json').read_text(encoding='utf-8')
    )
    readme = (REPO_ROOT / 'README.md').read_text(encoding='utf-8')

    documented = {
        match['option']: match['value']
        for match in DOCUMENTED_DEFAULT.finditer(readme)
    }
    assert documented, 'no documented defaults found; has the format changed?'

    mismatches = []
    for option, stated in documented.items():
        if option not in cookiecutter:
            mismatches.append(f'{option}: documented but not in the template')
            continue

        actual = cookiecutter[option]
        # A list in cookiecutter.json is a choice field; the first entry
        # is what a user gets by default.
        if isinstance(actual, list):
            actual = actual[0]

        if str(actual) != stated:
            mismatches.append(
                f'{option}: README says {stated!r}, actual {actual!r}'
            )

    assert not mismatches, 'README defaults are out of date:\n' + '\n'.join(
        mismatches
    )


# vim: fenc=utf-8
# vim: filetype=python
