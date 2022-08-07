# cookiecutter-py

🐍 Modern Python project Cookiecutter template

---

Each time you start a new Python project, you shouldn't start from scratch.
Ideally, you'd start with a standard project structure and set of tools and
integrations to help facilitate writing quality Python code.

This modern Python [Cookiecutter](https://github.com/audreyr/cookiecutter)
template is the tool that will help you do just that.

## Features

- [`poetry`](https://poetry.eustace.io) to manage dependencies
- [`structlog`](https://www.structlog.org/en/stable) for logging
- [`mypy`](https://mypy-lang.org) for static typing
- [`pytest`](https://github.com/pytest-dev/pytest), [`hypothesis`](https://github.com/HypothesisWorks/hypothesis), [`mutmut`](https://github.com/boxed/mutmut) for testing
  - [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) for coverage reports
  - [`pytest-mock`](https://github.com/pytest-dev/pytest-mock/) for mocks
  - [`pytest-xdist`](https://github.com/pytest-dev/pytest-xdist) for distributed testing
- [`tox`](https://tox.readthedocs.org/en/latest/) for testing automation
- [`sphinx`](http://www.sphinx-doc.org/en/master/) for docs
- [`pdb++`](https://github.com/pdbpp/pdbpp) for debugging
- [`konch`](http://konch.readthedocs.org/en/latest/) for shell configuration w/ [`ipython`](https://ipython.org) support
- [`pre-commit`](https://pre-commit.com) hooks with various hooks (mypy / black / flake8) configured
- [`dockerfile`](https://www.docker.com/) for development, testing, and production
- custom [`makefile`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/master/%7B%7Bcookiecutter.package_name%7D%7D/Makefile) (run make help)
- stay up-to-date w/ configured [`dependabot`](https://dependabot.com/)
- [`github-actions`](https://github.com/features/actions) with ci, publish to pypi workflows w/ draft-releaser workflow
- [`codecov`](https://codecov.io) (optional) integration for code coverage

## Installation

install [dependencies](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```bash
python3 -m pip install --user cookiecutter
```

After installing Cookiecutter, create the project:

```bash
cookiecutter gh:ryankanno/cookiecutter-py
```

## Details

Coming soon to a README near you!

## TODO

- add mutmut example to template
- add hypothesis example to template
- run pre-commit in github-actions (currently runs flake8 / black directly)
- clean up tox integration
- remove bump2version for dunamai
- add typeguard
- version releases
- integrate [earthly](https://github.com/earthly/earthly)
- darglint
- update details
  - include cookiecutter var descriptions

## License

MIT. See [LICENSE](https://github.com/ryankanno/cookiecutter-py/blob/main/LICENSE) for deets.
