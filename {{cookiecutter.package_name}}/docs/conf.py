# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys


sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '{{cookiecutter.package_name}}'
project_copyright = '2024, {{cookiecutter.author_name}}'
author = '{{cookiecutter.author_name}}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'myst_parser',
    {%- if cookiecutter.sphinx_theme == 'sphinx-wagtail-theme' -%}
    '{{ cookiecutter.sphinx_theme|replace('-', '_') }}'
    {%- endif %}
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

{% if cookiecutter.sphinx_theme == 'sphinx-press-theme' %}
html_theme = 'press'
{% else %}
html_theme = '{{ cookiecutter.sphinx_theme|replace('-', '_') }}'
{% endif %}

html_static_path = ['_static']
{% if cookiecutter.sphinx_theme == 'sphinx-rtd-theme' -%}
html_context = {
    "display_github": True,
    "github_user": "{{ cookiecutter.project_url.split('/')[-2] }}",
    "github_repo": "{{ cookiecutter.project_url.split('/')[-1] }}"
}
{% endif -%}
