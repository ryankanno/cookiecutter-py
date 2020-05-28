# cookiecutter-py

This is a fairly opinionated Python [cookiecutter](https://github.com/audreyr/cookiecutter) template.

Heavily influenced by

  * [py-skeleton-templates](https://github.com/ryankanno/py-skeleton-templates)
  * [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

Every time you start a new Python project, you shouldn't be starting from
scratch. Ideally, you'd start with a decent set of tooling / integrations to
help facilitate writing good code.

## Features

  * [Poetry](https://poetry.eustace.io): Python Dependency Management and Packaging
  * [Tox](https://tox.readthedocs.org/en/latest/): Standardized testing across different Python versions and interpreters
  * [Bump2version](https://github.com/c4urself/bump2version): Version-bumping
  * [Konch](http://konch.readthedocs.org/en/latest/): Configuration for your Python shell
  * Testing using [Pytest](http://pytest.org/latest/) with support for
  * [Pre-commit] hooks with checks for
    * [Mypy](http://mypy-lang.org)
    * Code formatting using [Black](https://black.readthedocs.io/en/latest/)
  * Documentation with [Sphinx](http://sphinx-doc.org/)
  * custom [Makefile](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/master/%7B%7Bcookiecutter.package_name%7D%7D/Makefile)
  * [MIT License](http://opensource.org/licenses/MIT)
