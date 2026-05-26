# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import subprocess
import sys


sys.path.insert(0, os.path.abspath('..'))


def _detect_commit_short() -> str:
    sha = os.environ.get('GITHUB_SHA', '')
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return sha[:7] if sha else ''


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '{{cookiecutter.package_name}}'
project_copyright = '2024, {{cookiecutter.author_name}}'
author = '{{cookiecutter.author_name}}'

_commit_short = _detect_commit_short()
if _commit_short:
    project_copyright = f'{project_copyright} · build {_commit_short}'
    copyright = project_copyright

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
{% if cookiecutter.sphinx_theme == 'furo' %}

html_css_files = ['version-switcher.css']
html_js_files = ['version-switcher.js']

html_sidebars = {
    '**': [
        'sidebar/brand.html',
        'sidebar/search.html',
        'sidebar/scroll-start.html',
        'sidebar/navigation.html',
        'sidebar/ethical-ads.html',
        'sidebar/scroll-end.html',
        'sidebar/version-selector.html',
        'sidebar/variant-selector.html',
    ],
}

_repo_url = '{{cookiecutter.project_url}}'
_github_mark_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
    'width="1em" height="1em" fill="currentColor" aria-hidden="true">'
    '<path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 '
    '5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49'
    '-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
    '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78'
    '-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 '
    '0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53'
    '-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 '
    '3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 '
    '0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>'
    '</svg>'
)

html_theme_options = {
    'source_repository': _repo_url,
    'source_branch': 'main',
    'source_directory': 'docs/',
    'footer_icons': [
        {
            'name': 'GitHub',
            'url': _repo_url,
            'html': _github_mark_svg,
            'class': '',
        },
    ],
}
{% endif -%}
