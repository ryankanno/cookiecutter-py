# cookiecutter-py

This is a fairly opinionated Python cookiecutter for
[Cookiecutter](https://github.com/audreyr/cookiecutter).

Heavily influenced by

  * [py-skeleton-templates](https://github.com/ryankanno/py-skeleton-templates)
  * [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

Every time you start a new Python project, you shouldn't be starting from
scratch. Ideally, you'd start with a decent set of tooling / integrations to
help facilitate writing good code.

One of these days, I'll write about all the Python tools that I use.

## Dependencies

While you don't necessarily need all these tools installed to use this
cookiecutter, it'll help you take full advantage of it.

  * [pyenv](https://github.com/yyuu/pyenv)
  * [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
  * [teamocil](https://github.com/remiprev/teamocil)
  * [konch](https://github.com/sloria/konch)
  * [tox](https://bitbucket.org/hpk42/tox)

## What you're getting

  * [MIT License](http://opensource.org/licenses/MIT)
  * decent [setup.py](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/master/%7B%7Bcookiecutter.package_name%7D%7D/setup.py)
  * [pyenv virtualenv](https://github.com/yyuu/pyenv-virtualenv) named `cookiecutter.package_name`
  * [teamocil](http://www.teamocil.com/) tmux yml file
  * [konch](http://konch.readthedocs.org/en/latest/) configuration file
  * custom [makefile](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/master/%7B%7Bcookiecutter.package_name%7D%7D/Makefile)
  * [pytest](http://pytest.org/latest/) integration
  * [coverage](http://coverage.readthedocs.org/en/latest/) integration
  * [flake8](http://flake8.readthedocs.org/en/latest/) integration
  * [sphinx](http://sphinx-doc.org/) integration
  * [tox](https://tox.readthedocs.org/en/latest/) integration
  * [travis-ci](https://travis-ci.org/) .yml file
