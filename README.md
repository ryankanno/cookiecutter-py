<h3 align="center">cookiecutter-py</h3>

<div align="center">
  <p>🐍 Modern Python project Cookiecutter template</p>
</div>

<div align="center">

[![GitHub Issues][github-issues-shield]][github-issues-url]
[![GitHub Pull Requests][github-prs-shield]][github-prs-url]
[![License][project-license-shield]][project-license-url]

</div>

<div align="center">

[**Explore the latest docs »**][project-docs]

</div>

---

Each time you start a new Python project, you shouldn't start from scratch.
Ideally, you'd start with a standard project structure and set of tools and
integrations to help facilitate writing quality Python code.

This modern Python [Cookiecutter](https://github.com/audreyr/cookiecutter)
template is the tool that will help you do just that.

---

<!-- FEATURES -->
## ✨ Features

- [`uv`](https://github.com/astral-sh/uv) to manage dependencies
- [`structlog`](https://www.structlog.org/en/stable) for logging
- [`mypy`](https://mypy-lang.org) for static typing
- [`pytest`](https://github.com/pytest-dev/pytest), [`hypothesis`](https://github.com/HypothesisWorks/hypothesis), [`mutmut`](https://github.com/boxed/mutmut) for testing

  - [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) for coverage reports
  - [`pytest-mock`](https://github.com/pytest-dev/pytest-mock/) for mocks
  - [`pytest-xdist`](https://github.com/pytest-dev/pytest-xdist) for distributed testing
  - [`pytest-randomly`](https://github.com/pytest-dev/pytest-randomly) to randomly order tests

- [`tox`](https://tox.readthedocs.org/en/latest/) for testing automation
- [`sphinx`](http://www.sphinx-doc.org/en/master/) for docs
  - [`myst-parser`](https://github.com/executablebooks/MyST-Parser) for markdown docs
  - selectable theme
- [`pdbp`](https://github.com/mdmintz/pdbp) for debugging
- [`konch`](http://konch.readthedocs.org/en/latest/) for shell configuration w/ [`ipython`](https://ipython.org) support
- [`pre-commit`](https://pre-commit.com) hooks with various hooks (mypy / black / [`ruff`](https://github.com/astral-sh/ruff) / [`deptry`](https://github.com/fpgmaas/deptry))
- [`dockerfile`](https://www.docker.com/) for development, testing, and production
- [`dunamai`](https://github.com/mtkennerly/dunamai) for versioning
- custom [`Justfile`](https://github.com/casey/just) (run `just`)
- stay up-to-date w/ configured [`dependabot`](https://dependabot.com/)
- [`github-actions`](https://github.com/features/actions) with ci (leveraging [`tox`](https://tox.readthedocs.org/en/latest/)), publish to pypi workflows w/ [`release-drafter`](https://github.com/release-drafter/release-drafter) integration

  - [`ci`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/ci.yml) workflow (leveraging [`tox`](https://tox.readthedocs.org/en/latest/))

    - optional [`codecov`](https://codecov.io) integration for code coverage

  - [`publish`](https://github.com/ryankanno/cookiecutter-py/blob/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/publish.yml) workflow (to [test.pypi.org](https://test.pypi.org) / [pypi.org](https://pypi.org)) w/ [`release-drafter`](https://github.com/release-drafter/release-drafter) integration
  - [`auto approve / merge`](https://github.com/ryankanno/cookiecutter-py/blob/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/auto-approve-merge-dependabot.yml) workflow
  - with these additional workflows:

    - [`codeql`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/codeql-analysis.yml)
    - [`hadolint`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/hadolint.yml)
    - [`pr-size-labeling`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/pr-size-labeler.yml)
    - [`commitlint`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/commitlint.yml)
    - [`trufflehog`](https://raw.githubusercontent.com/ryankanno/cookiecutter-py/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/workflows/trufflehog.yml)
- optional [`direnv`](https://github.com/direnv/direnv) .envrc (with [`use uv`](https://raw.githubusercontent.com/ryankanno/dotfiles/5ed45cfd8c387489fc0459eb1a485b2c21f3d159/dot_config/direnv/direnvrc) layout)

<!-- GETTING STARTED -->
## 🚀 Getting Started

### Prerequisites

Install [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```sh
uv add cookiecutter
# pip install cookiecutter
# pipenv install cookiecutter
```

**Optional**: Install [Cruft](https://github.com/cruft/cruft)

```sh
uv add cruft
# pip install cruft
# pipenv install cruft
```

## 🛠️ Usage

### Cookiecutter

```sh
cookiecutter gh:ryankanno/cookiecutter-py
```

**Note**: If you want to use the auto approve / merge Dependabot workflow, make
sure to create tags `major`, `minor`, `patch` so that Dependabot can tag its
PRs. The workflow won't merge anything with a `major` tag.

### Cruft (Optional)

```sh
cruft create https://github.com/ryankanno/cookiecutter-py/
```

<!-- DETAILS -->
## 🔍 Details

Coming soon to a README near you!

### Docker

To build the container:

```sh
DOCKER_BUILDKIT=1 docker build .
```

To run the container (if you've installed the defaults):

```sh
docker run <image_id or tag> python -m surf.surf
```

### Versioning

If you enable the PyPi workflow, versioning will happen via [`dunamai`](https://github.com/mtkennerly/dunamai) within the Github pipeline.

If instead, you prefer to version your package, please do it via ```uv version $(dunamai from any)``` as recommended in their [documentation](https://github.com/mtkennerly/dunamai#user-content-integration).

<!-- ROADMAP -->
## 🚧 Roadmap

See the [open issues](https://github.com/ryankanno/cookiecutter-py/issues) for a list of proposed features (and known issues).

<!-- TODO -->
## ☑️ TODO

- [ ] add mutmut example to template
- [ ] add hypothesis example to template
- [ ] add licenses
- [ ] add typeguard
- [ ] version releases
- [ ] update docs
  - [ ] include cookiecutter var descriptions
- [ ] add publish docs workflow
- [X] update default/initial template doc structure
- [X] investigate uv
- [X] migrate to uv
- [X] finalize v1.0.0

<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are very much appreciated.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-cookiecutter-feature`)
3. Commit your changes (`git commit -m 'Added a new feature'`)
4. Push to the feature branch (`git push origin feature/new-cookiecutter-feature`)
5. Open a PR! 🎆

<!-- LICENSE -->
## 📝 License

Distributed under the MIT License. See [`LICENSE`](https://github.com/ryankanno/cookiecutter-py/blob/main/LICENSE) for more information.

<!-- CONTACT -->
## 📫 Contact

Ryan Kanno - [@ryankanno][twitter-ryankanno-url]

Project Link: [https://github.com/ryankanno/cookiecutter-py][project-url]


[project-url]: https://github.com/ryankanno/cookiecutter-py
[project-docs]: https://ryankanno.github.io/cookiecutter-py/latest
[project-license-shield]: https://img.shields.io/github/license/ryankanno/cookiecutter-py
[project-license-url]: https://github.com/ryankanno/cookiecutter-py/blob/main/LICENSE
[github-issues-shield]: https://img.shields.io/github/issues/ryankanno/cookiecutter-py
[github-issues-url]: https://github.com/ryankanno/cookiecutter-py/issues
[github-prs-shield]: https://img.shields.io/github/issues-pr/ryankanno/cookiecutter-py
[github-prs-url]: https://github.com/ryankanno/cookiecutter-py/pulls
[twitter-ryankanno-url]: https://twitter.com/ryankanno
