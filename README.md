# cookiecutter-py

This is a fairly opinionated Python [cookiecutter](https://github.com/audreyr/cookiecutter) template.

Heavily influenced by

  * [py-skeleton-templates](https://github.com/ryankanno/py-skeleton-templates)
  * [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

Every time you start a new Python project, you shouldn't start from
scratch. Ideally, you'd start with a decent set of tooling / integrations to
help facilitate writing good Python code. This is the tool that will help you
do that.

## Features

  * [Poetry](https://poetry.eustace.io): Python Dependency Management and Packaging
  * [Tox](https://tox.readthedocs.org/en/latest/): Standardized testing across different Python versions and interpreters
  * [Bump2version](https://github.com/c4urself/bump2version): Version bumping
  * [Konch](http://konch.readthedocs.org/en/latest/): Configurations for your Python shell with support for
    * [IPython](https://ipython.org)
  * Logging configuration w/ [Structlog](https://www.structlog.org/en/stable/) integration
  * [Pdb++](https://github.com/pdbpp/pdbpp) support, an enhanced Python debugger
  * Testing using [Pytest](http://pytest.org/latest/) with support for
    * Coverage reports using [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
    * Mock support using [pytest-mock](https://github.com/pytest-dev/pytest-mock/)
    * Random test runs using [pytest-randomly](https://github.com/pytest-dev/pytest-randomly)
    * Distributed testing and loop-on-failing support using [pytest-xdist](https://github.com/pytest-dev/pytest-xdist)
  * [Pre-commit](https://pre-commit.com) hooks with checks for
    * [Mypy](http://mypy-lang.org)
    * Code formatting using [Black](https://black.readthedocs.io/en/latest/)
    * [Flake8](https://flake8.pycqa.org/en/latest/) style/quality
  * Documentation with [Sphinx](http://sphinx-doc.org/)
  * custom [Makefile](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/master/%7B%7Bcookiecutter.package_name%7D%7D/Makefile) (run make help)
  * [MIT License](http://opensource.org/licenses/MIT)
