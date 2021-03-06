import os

from setuptools import find_packages, setup

from {{cookiecutter.package_name}}.metadata import __version__


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fobj:
    README = fobj.read()


setup(
    name="{{cookiecutter.package_name}}",
    version=__version__,
    description="{{cookiecutter.short_description}}",
    long_description=README,
    classifiers=["Programming Language :: Python :: 3"],
    author="{{cookiecutter.author_name}}",
    author_email="{{cookiecutter.author_email}}",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "build": ["wheel<1"],
        "lint": ["flake8<4", "black==19.3b0"{%- if cookiecutter.use_pylint == "y" %}, "pylint<3"{%- endif%}{%- if cookiecutter.use_mypy == "y" %}, "mypy<0.800"{%- endif%}],
        "test": ["pytest<5", "pytest-cov<3"],
    },
    zip_safe=False,
)
