#!/usr/bin/env just --justfile

set quiet

poetry := 'poetry'

[private]
default:
    just --list

# Remove build artifacts (build, dist, .egg)
[private]
clean-build:
    rm -fr build/
    rm -fr dist/
    rm -fr .eggs/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +

# Remove Python artifacts (.pyc, .pyo, __pycache__)
[private]
clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +

# Remove test artifacts (.tox, .coverage, coveragexml)
[private]
clean-test:
    rm -fr .tox/
    rm -f .coverage
    rm -f coverage.xml
    rm -fr htmlcov/

# Remove docs
[private]
clean-docs:
    rm -fr .tox/docsout

# Remove build, Python, test artifacts, and docs
clean: clean-docs clean-build clean-pyc clean-test

# Check code coverage with current Python
coverage:
    {{poetry}} run pytest --cov --cov-config=pyproject.toml --cov-append --cov-report term-missing --doctest-modules -ra -q -n auto
    {{poetry}} run coverage report -m
    {{poetry}} run coverage html
    open htmlcov/index.html

# Generate Sphinx documentation (tox:docs)
[no-quiet]
docs: clean-docs
    just tox run -e docs

# Package
dist: clean
    {{poetry}} build

# Install package to current Python's site-package
install: clean
    {{poetry}} install

# Lint (tox:lint)
lint:
    just tox run -e lint

# Lint fix (tox:lint-fix)
lint-fix:
    just tox run -e lint-fix

# Runs tests (tox:tests)
tests:
    just tox run-parallel -m tests

# Runs pre-commit (tox:pre-commit)
pre-commit:
    just tox run -e pre-commit

# Runs tox
tox *TOX_ARGS:
    {{poetry}} run tox {{ TOX_ARGS }}
