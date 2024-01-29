import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fobj:
    README = fobj.read()


setup(
    name="python_project_template",
    version="0.1.0",
    description="Template to generate Python projects with cookiecutter",
    long_description=README,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Pytest",
        "Typing :: Typed",
    ],
    author="Mendix Cloud Value Added Services Team",
    author_email="dis_valueaddedservices@mendix.com",
    packages=[],
    install_requires=["cookiecutter>2.1.1,<3"],
    extras_require={
        "lint": [
            "flake8<7",
            "black<24",
            "pylint<4",
            "mypy<2"
        ],
        "test": [
            "pytest<9",
            "pytest-cookies<1",
            "pytest-cov<5",
        ],
    },
    zip_safe=False,
)
