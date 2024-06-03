<h3 align="center">cookiecutter-py</h3>

<div align="center">
  <p>🐍 Modern Python project Cookiecutter template</p>
</div>

<div align="center">

[![GitHub Issues][github-issues-shield]][github-issues-url]
[![GitHub Pull Requests][github-prs-shield]][github-prs-url]
[![License][license-shield]][license-url]

</div>

<div align="center">
  <p><a href="http://ryankanno.github.io/cookiecutter-py/latest"><strong>Explore the latest docs »</strong></a></p>
</div>

---

Each time you start a new Python project, you shouldn't start from scratch.
Ideally, you'd start with a standard project structure and set of tools and
integrations to help facilitate writing quality Python code.

This modern Python [Cookiecutter](https://github.com/audreyr/cookiecutter)
template is the tool that will help you do just that.

<!-- FEATURES -->
## ✨ Features

- [`poetry`](https://poetry.eustace.io) to manage dependencies
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
- [`pdb++`](https://github.com/pdbpp/pdbpp) for debugging
- [`konch`](http://konch.readthedocs.org/en/latest/) for shell configuration w/ [`ipython`](https://ipython.org) support
- [`pre-commit`](https://pre-commit.com) hooks with various hooks (mypy / black / [`ruff`](https://github.com/astral-sh/ruff))
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
- optional [`direnv`](https://github.com/direnv/direnv) .envrc (with pyenv layout)

<!-- GETTING STARTED -->
## 🚀 Getting Started

### Prerequisites

Install [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```sh
pip install cookiecutter
# poetry add cookiecutter
# pipenv install cookiecutter
```

**Optional**: Install [Cruft](https://github.com/cruft/cruft)

```sh
pip install cruft
# poetry add cruft
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

If instead, you prefer to version your package, please do it via ```poetry version $(dunamai from any)``` as recommended in their [documentation](https://github.com/mtkennerly/dunamai#user-content-integration).

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
- [ ] update default/initial template doc structure
- [ ] add publish docs workflow
- [ ] investigate uv
- [ ] plan for 1.0

<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **extremely appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## 📝 License

Distributed under the MIT License. See [`LICENSE`](https://github.com/ryankanno/cookiecutter-py/blob/main/LICENSE) for more information.

<!-- CONTACT -->
## 📫 Contact

Ryan Kanno - @ryankanno

Project Link: [https://github.com/ryankanno/cookiecutter-py](https://github.com/ryankanno/cookiecutter-py)

<!-- ACKNOWLEDGEMENTS -->
## 🙏 Acknowledgements

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[github-issues-shield]: https://img.shields.io/github/issues/ryankanno/cookiecutter-py
[github-issues-url]: https://github.com/ryankanno/cookiecutter-py/issues
[github-prs-shield]: https://img.shields.io/github/issues-pr/ryankanno/cookiecutter-py
[github-prs-url]: https://github.com/ryankanno/cookiecutter-py/pulls
[license-shield]: https://img.shields.io/github/license/ryankanno/cookiecutter-py
[license-url]: https://github.com/ryankanno/cookiecutter-py/blob/main/LICENSE
