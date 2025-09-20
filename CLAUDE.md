# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern Python Cookiecutter template project that generates standardized Python project structures. The repository contains both the cookiecutter template source code and a generated template directory (`{{cookiecutter.package_name}}/`) that serves as the blueprint for new projects.

## Architecture

- **Root project**: The cookiecutter template itself with its own test suite
- **Template directory**: `{{cookiecutter.package_name}}/` contains the actual template files that get generated
- **Hooks**: Pre/post generation scripts in `hooks/` directory
- **Configuration**: `cookiecutter.json` defines template variables and defaults

The template generates projects with:
- `uv` for dependency management
- `tox` for testing across Python versions
- `pytest` with coverage, xdist, and other plugins
- `ruff` for linting and formatting
- `mypy` for type checking
- `sphinx` for documentation
- Pre-commit hooks and GitHub Actions workflows

## Development Commands

All commands use `uv` as the package manager and `just` as the task runner.

### Primary Commands
- `just tests` - Run tests across all Python versions using tox
- `just lint` - Run linting checks (ruff, mypy, etc.)
- `just lint-fix` - Auto-fix linting issues where possible
- `just coverage` - Generate coverage report and open HTML report
- `just docs` - Build Sphinx documentation
- `just clean` - Remove all build artifacts

### Tox Commands
- `just tox run -e py311` - Run tests on Python 3.11
- `just tox run -e py312` - Run tests on Python 3.12
- `just tox run -e pre-commit` - Run pre-commit hooks
- `just tox run-parallel -m tests` - Run tests in parallel across Python versions

### Testing
The project tests the cookiecutter template generation process:
- Tests use `pytest-cookies` to test cookiecutter generation
- Tests verify generated projects build and work correctly
- Coverage configured to track `hooks/` directory

### Key Configuration Files
- `pyproject.toml` - Main project configuration, dependencies, and tool settings
- `tox.ini` - Multi-Python testing configuration
- `Justfile` - Task runner commands
- `cookiecutter.json` - Template variables and defaults

When working with this codebase, be aware that changes may affect both the cookiecutter template itself and the generated project template in `{{cookiecutter.package_name}}/`.
