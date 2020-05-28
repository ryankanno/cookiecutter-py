.PHONY: help

export PYTHONPATH=$(shell pwd)

help: ## Prints out help dialog
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`); \
	for help_line in $${help_lines[@]}; do  \
		IFS=$$'#' ; \
		help_split=($$help_line); \
		help_command=`echo $${help_split[0]%%:*}`; \
		help_info=`echo $${help_split[2]%%}`; \
		printf "%-30s %s\n" $$help_command $$help_info; \
	done; \

clean: clean-docs clean-build clean-pyc clean-test ## Remove build, Python, test artifacts, and docs

clean-build: ## Remove build artifacts (build, dist, .egg)
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-docs: ## Remove docs
	rm -f docs/{{ cookiecutter.package_name }}.rst
	rm -f docs/modules.rst

clean-pyc: ## Remove Python artifacts (.pyc, .pyo, __pycache__)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Remove test artifacts (.tox, .coverage, coveragexml)
	@rm -fr .tox/
	@rm -f .coverage
	@rm -f coverage.xml
	@rm -fr htmlcov/

coverage: ## Check code coverage with current Python
	poetry run pytest --cov={{ cookiecutter.package_name}} tests/
	poetry run coverage report -m
	poetry run coverage html
	open htmlcov/index.html

docs: clean-docs  ## generate Sphinx documentation
	sphinx-apidoc -o docs/ {{ cookiecutter.package_name }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

dist: clean ## Package {{ cookiecutter.package_name }}
	poetry build
	ls -l dist

install: clean ## Install package to current Python's site-package
	poetry install

lint: ## Check style with flake8
	poetry run flake8 {{ cookiecutter.package_name }} tests

release: clean ## Package and upload a release
	ls -al

test: ## Runs test with current Python
	poetry run pytest tests/

test-all: ## Runs test against all Pythons with tox
	tox

