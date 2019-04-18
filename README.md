# python-project-template

A [`cookiecutter`](https://github.com/audreyr/cookiecutter) based Python
project template.

## Usage

In the below sections it is explained how to generate a new Python package with
this project. When generating a new package, the tool will request a series of
inputs, such as the package name, description, author, whether to include
certain tooling, etc.

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
verbosit, etc.), run `cookiecutter --help`.

### Remove clutter

In order to be able to test that the package is generated correctly and linting
and tests can be run, there is a `dummy.py` and a corresponding `test_dummy.py`
file generated. This is exactly what the name suggests and should be removed.

### Pushing to Git

Make sure you have created a new repository in GitLab/GitHub/etc. already.

After having the desired package generated you can
* Run `git init` in the new project root and add the existing remote repository
with `git remote add origin <repository URL>`
* Or if you have the empty repository already cloned on your machine, copy the
generated files to the cloned local repository
* Then all you have to do is push

## About the contents of this repository

This project makes use of the following tools (similarly to the generated
Python package - see below):
* `make`
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
plugin, `pytest-cookies` is used. This provides a `cookies` fixture, which is
injected into the test cases during runtime, making it really easy to test-run
the `cookiecutter` template in an auto-generated location.

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
    * `pylint` - linting, error and duplication detection and very much
    customizable; the generated project contains a minimal, but decent
    `pylintrc` configuration file; its usage is optional, can be decided upon
    project generation, however highly recommended and turned on by default
    * `mypy` - type checker, the de facto standard at the moment; its usage is
    optional, can be decided upon project generation, however highly
    recommended and turned on by default
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

_Note: the targets `lint`, `test` and `build` have a corresponding
`install_<target>_requirements` target to install extra dependencies. These are
individually defined in the generated project's `setup.py` as well as extra
requirements. There is no need to call the install targets on their own, they
are called automatically in their related main target._

### Future extension

New linters can be easily added by extending the `Makefile`, potentially made
optional (just as with `pylint` or `mypy`).

Currently in the created project there is only one `test` target which is
intendet to be used to run a set of automated tests in the "commit phase".
However eventually there should be more testing targets created, thus
separating different levels of automated tests, such as
* Integration tests (`test-integration`) - automatically verifying the
application is piped correctly to other system components
* Acceptance tests (`test-acceptance` target) - automatically verifying
functional and non-functional requirements, potentially in a BDD style
* Capacity tests (`test-capacity` target) - automatically verifying that an
application is able to handle load according to requirements
* Security (`security` target), to run some automated security tooling
(eg. Snyk or BlackDuck) to reveal potential vurnelabilities in the application
code itself or introduced by dependencies

In addition to this we could introduce automated documentation generation in
the created project, using [Sphinx](http://www.sphinx-doc.org/en/master/) via
a `make docs` target. For this we will need some storage to be able to host the
generated docs and push to it from Python projects upon a successful master
build.
