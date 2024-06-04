.. {{cookiecutter.package_name}} documentation master file, created by
   sphinx-quickstart on Tue May 28 11:47:08 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

Welcome to {{cookiecutter.package_name}}'s documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

    getting_started <getting_started/getting_started>
    usage <usage/usage>
    roadmap <roadmap/roadmap>
    todo <todo/todo>

{{cookiecutter.short_description}}

.. include:: ../README.md
   :parser: myst_parser.sphinx_
   :start-after: Features
   :end-before: ## 🚀 Getting Started
.. include:: ../LICENSE


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
