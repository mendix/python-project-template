# python-project-template

![Test status](https://github.com/matyaskuti/python-project-template/actions/workflows/python-app.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [`cookiecutter`](https://github.com/audreyr/cookiecutter) based Python
project template.

This is an opinionated template, based on useful defaults that we like to have
when creating new projects. We include a pre-built Makefile, with rules for
linting and test, scaffolded unit tests, and tools for building wheels,
amongst other things.

This project is open source because we think it might be useful to other
engineers. However, Mendix does not officially support this project.

## License

This project is licensed under the MIT license.

## Usage - new project

In the below sections it is explained how to generate a new Python package with
this project. When generating a new package, the tool will request a series of
inputs, such as the package name, description, author, tooling such as
package management, etc.

### By cloning this repo

1. Clone this repository on your local machine
2. In the local repository root, run `make generate`
    This will create the new project in the repo root, in order to specify a
    target directory, run with `make generate TARGET_DIR="/path/to/dir"`

_Note: using the above `make generate` target, the `cookiecutter` package will
be installed automatically._

### By manually installing `cookiecutter`

1. Install `cookiecutter` with `pip install cookiecutter`
2. Run `cookiecutter <repository URL>`

To see what options `cookiecutter` offers (eg. output/target directory,
verbosity, etc.), run `cookiecutter --help`.

### Remove clutter

In order to be able to test that the package is generated correctly and linting
and tests can be run, there is a `dummy.py` and a corresponding `test_dummy.py`
file generated. This is exactly what the name suggests and should be removed.

## About the contents of this repository

This project makes use of the following tools (similarly to the generated
Python package - see below):
* `make`
* `poetry`
* `cookiecutter`
* `pytest`
* `pytest-cookies`
* `pylint`
* `black`
* `flake8`
* `mypy`

These are the most notable components:
* `{{cookiecutter.package_name}}` - the directory containing the actual
blueprint of the project to be generated, file names and contents are
essentially Jinja2 templates, which are filled in by `cookiecutter`
* `hooks` - contains pre-generation and post-generation Python scripts to
ensure the new project contains what it needs to contain
* `tests` - contains a set of automated tests that ensure project generation is
correct
* `cookiecutter.json` - configuration file for `cookiecutter` with default
values of project parameters

In order to easily test proper generation of a Python project, a `pytest`
plugin, [`pytest-cookies`](https://github.com/hackebrot/pytest-cookies) is
used. This provides a `cookies` fixture, which is injected into the test cases
during runtime, making it really easy to test-run the `cookiecutter` template
in an auto-generated location.

While the project uses [Poetry](https://python-poetry.org/) as a package
manager, to install and use it (ie. to run `make generate`), does not require
Poetry, only Pip (which is assumed to be part of most standard Python
installations). Only contributing requires Poetry.

## About the generated Python project

One of the goals of this, besides providing uniform tooling to all new Python
packages is to define and create a common interface for all projects so they
can be plugged in to the same CI/CD pipeline (template).

Below are the main `make` targets and the tools used within:

* `lint` - to ensure compliance to coding standards
    * `flake8` - PEP8 style checker, to ensure a standard code format that is
    familiar to all Python developers and easy to read
    * `black` - also a PEP8 checker and autoformatter; because PEP8 compliance
    still leaves a lot of flexibility and there are as many preferences as
    developers, we use this tool because it is already opinionated so you don't
    have to be
    * `isort` - linter and formatter specialized for imports
    * `pylint` - linting, error and duplication detection and very much
    customizable; the generated project contains a minimal, but decent set of
    configuration
    * `mypy` - type checker, the de facto standard at the moment
* `format` - to easily comply with the above standards at the push of a button
    * `black` - because of the reasons mentioned above
* `test` - to verify functionality at the smallest level of granularity (unit)
    * `pytest` - at the moment this is one of the best test-runner tools
    available; besides that it provides a powerful test fixture mechanism
    (this should be used sparingly though, if the builtin `unittest` library
    doesn't suffice - although this is a matter of taste to some extent)
    * `pytest-cov` - plugin of `pytest` to provide coverage metrics
* `clean` - to clean the working directory by removing generated files,
reports, etc.
* `build` - to create a standard, distributable Python package
    * `wheel` - this is the current standard for creating distributables

_Note: the targets `lint` and `test` have a corresponding
`install_<target>_requirements` target to install extra dependencies. These are
individually defined in the generated project's `pyproject.toml` as well, as
extra requirements. There is no need to call the install targets on their own,
they are called automatically in their related main target._

### Dependency and package management

A single ``pyproject.toml`` file is used for the generated project's
definition, packaging and tooling configuration.
When generating the project, the `build_system` parameter decides whether the
created Python package use [Poetry](https://python-poetry.org/) or
[Setuptools](https://setuptools.pypa.io/) for dependency management and as a
build backend: it defaults to Poetry, if any other value is provided then
Setuptools will be used.

Picking either will be reflected in the ``pyproject.toml`` and the
``Makefile``.
