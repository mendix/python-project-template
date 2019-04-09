import os

from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fobj:
    README = fobj.read()


setup(
    name="python-project-template",
    version="0.1.0",
    description="Template to generate Python projects with cookiecutter",
    long_description=README,
    classifiers=[],
    author="Mendix Cloud Team",
    author_email="devops@mendix.com",
    packages=[],
    install_requires=["cookiecutter>=1.4<2"],
    zip_safe=False,
)
