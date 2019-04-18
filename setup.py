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
        "Programming Language :: Python :: 3",
    ],
    author="Mendix Cloud Value Added Services Team",
    author_email="dis_valueaddedservices@mendix.com",
    packages=[],
    install_requires=["cookiecutter>=1.4<2"],
    extras_require={
        "lint": [
            "flake8<4",
            "black==19.3b0",
            "pylint<3",
            "mypy<0.800"
        ],
        "test": [
            "pytest<5",
            "pytest-cookies<1",
            "pytest-cov<3",
        ],
    },
    zip_safe=False,
)
