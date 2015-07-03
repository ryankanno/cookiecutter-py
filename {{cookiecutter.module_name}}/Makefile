.PHONY: help

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

clean-all: ## Remove build, Python, and test artifacts
	clean-build clean-pyc clean-test

clean-build: ## Remove build artifacts (build, dist, .egg)
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## Remove Python artifacts (.pyc, .pyo, __pycache__)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Remove test artifacts (.tox, .coverage, coveragexml)
	@rm -fr .tox/
	@rm -f .coverage
	@rm -ff coverage.xml
	@rm -fr htmlcov/

coverage: ## Check code coverage with current Python
	coverage run --source {{ cookiecutter.module_name }} setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx documentation
	rm -f docs/{{ cookiecutter.module_name }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.module_name }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

dist: clean ## Package {{ cookiecutter.module_name }}
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## Install package to current Python's site-package
	python setup.py install

lint: ## Check style with flake8
	python setup.py flake8
	flake8 tests

release: clean ## Package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

test: ## Runs test with current Python
	python setup.py test

test-all: ## Runs test against all Pythons with tox
	tox

