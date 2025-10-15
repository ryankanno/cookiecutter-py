# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern Python Cookiecutter template project that generates standardized Python project structures. The repository contains both the cookiecutter template source code and a generated template directory (`{{cookiecutter.package_name}}/`) that serves as the blueprint for new projects.

## Architecture

### Dual Structure
- **Root project**: The cookiecutter template itself with its own test suite and tooling
- **Template directory**: `{{cookiecutter.package_name}}/` contains Jinja2-templated files that get rendered when users run cookiecutter
- **Hooks**: Pre/post generation Python scripts in `hooks/` directory that customize generated projects based on user choices
- **Configuration**: `cookiecutter.json` defines template variables, defaults, and choices (like sphinx theme options)

### Critical Architectural Patterns
- **Template exclusions**: `pyproject.toml` excludes `{{cookiecutter.package_name}}/` from mypy/black/ruff to prevent linting unrendered Jinja2 templates
- **Post-generation hooks**: `hooks/post_gen_project.py` conditionally removes files based on user selections (e.g., direnv, GitHub workflows, author files)
- **Test strategy**: Uses `pytest-cookies` plugin to test actual template generation, verifying that cookiecutter variables are properly substituted and expected files exist

The template generates projects with:
- `uv` for dependency management
- `tox` for testing across Python versions (3.10, 3.11, 3.12, PyPy)
- `pytest` with coverage, xdist, randomly, mock, and hypothesis
- `ruff` for linting and formatting
- `mypy` for type checking
- `sphinx` for documentation with selectable themes
- Pre-commit hooks with comprehensive tooling (detect-secrets, commitlint, bashate, typos, deptry)
- GitHub Actions workflows (CI, CodeQL, publish to PyPI, auto-approve/merge Dependabot)
- Docker configuration for development and production

## Development Commands

All commands use `uv` as the package manager and `just` as the task runner.

### Primary Commands
- `just tests` - Run tests across all Python versions using tox (fast, no coverage)
- `just tests -- path/to/test.py` - Run specific test file
- `just tests -- --durations=10` - Show slowest 10 tests
- `just coverage` - Run tests with comprehensive coverage analysis
- `just lint` - Run ruff linting checks via tox
- `just lint --fix` - Auto-fix ruff linting issues
- `just pre-commit` - Run all pre-commit hooks
- `just docs` - Build Sphinx documentation
- `just clean` - Remove all build, test, and documentation artifacts
- `just install` - Install dependencies using uv
- `just dist` - Build distribution packages

### Tox Environments
- `just tox run -e py310` - Run tests on Python 3.10
- `just tox run -e py311` - Run tests on Python 3.11
- `just tox run -e py312` - Run tests on Python 3.12
- `just tox run -e coverage-py312` - Run tests with coverage on Python 3.12
- `just tox run -e pre-commit` - Run pre-commit hooks
- `just tox run -e docs` - Build documentation
- `just tox run-parallel -m tests` - Run all test environments in parallel
- `just tox run-parallel -m coverage` - Run all coverage environments in parallel

### Testing
The project tests the cookiecutter template generation process:
- Tests use `pytest-cookies` plugin to test actual cookiecutter generation
- Tests verify that all cookiecutter variables (e.g., `{{cookiecutter.package_name}}`) are properly substituted in generated files
- Tests verify expected files exist based on user configuration choices
- Tests verify post-generation hooks correctly remove conditional files
- Parameterized tests cover different configuration combinations (codecov, uv version, tox version, sphinx theme)
- Coverage tracks `hooks/` directory to ensure post-generation scripts are tested

### Key Configuration Files
- `pyproject.toml` - Main project configuration, dependencies, tool settings (mypy, ruff, pytest, coverage)
- `tox.ini` - Multi-Python testing configuration with test/coverage/lint/docs environments
- `Justfile` - Task runner commands wrapping common operations
- `cookiecutter.json` - Template variables, defaults, and choices for template generation
- `hooks/post_gen_project.py` - Post-generation script that conditionally removes files based on user selections
- `hooks/pre_gen_project.py` - Pre-generation validation script

## Important Considerations

When working with this codebase, be aware that changes may affect both:
1. The cookiecutter template infrastructure itself (tests, hooks, root configuration)
2. The generated project template in `{{cookiecutter.package_name}}/` (files that end users will receive)

When modifying template files in `{{cookiecutter.package_name}}/`, ensure cookiecutter variables use proper Jinja2 syntax and test with `just tests` to verify substitution works correctly.
