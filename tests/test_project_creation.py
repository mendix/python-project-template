"""Test Python project creation with `cookiecutter`.

This test module makes use of `pytest` fixtures and the `pytest-cookies`
fixture plugin (https://github.com/hackebrot/pytest-cookies). Therefore if
you encounter a `cookies` parameter in a test-function fear not, it is a
`cookiecutter` test fixture, injected by `pytest`.
This plugin makes it a lot more convenient to invoke `cookiecutter` than
calling it as an external process, having to programatically complete the
project generator wizard.
"""
import abc
import glob
from collections.abc import Collection

from pytest_cookies.plugin import Cookies, Result

from .util import (
    check_output_in_result_dir,
    generate_temporary_project,
    inside_directory_of,
)

DEFAULT_PROJECT_NAME = "pymx"
ALL_SOURCE = f"{DEFAULT_PROJECT_NAME} tests"


def assert_successful_creation(result: Result) -> None:
    assert result.project.isdir()
    assert result.exit_code == 0
    assert result.exception is None


def assert_expected_files_exist(
    result: Result,
    files: Collection[str],
) -> None:
    created_files = [f.basename for f in result.project.listdir()]
    for fname in files:
        assert fname in created_files


def assert_expected_files_do_not_exist(
    result: Result,
    files: Collection[str],
) -> None:
    with inside_directory_of(result):
        for cleaned_up in files:
            for filename in glob.glob("./**", recursive=True):
                assert cleaned_up not in filename


def assert_expected_lines_are_in_output(
    expected_lines: Collection[str],
    output: str,
) -> None:
    for line in expected_lines:
        assert line in output


def assert_project_file_contains(
    result: Result, file_name: str, expected_lines: Collection[str]
) -> None:
    with inside_directory_of(result):
        with open(file_name, encoding="utf-8") as fobj:
            content: list[str] = fobj.readlines()
            for line in expected_lines:
                assert f"{line}\n" in content


class Context(abc.ABC):
    @property
    def extra_files(self) -> tuple[str, ...]:
        return ()

    @property
    @abc.abstractmethod
    def runner(self) -> str:
        ...

    @abc.abstractmethod
    def install(self, extra: str) -> str:
        ...

    @property
    def project_files(self) -> tuple[str, ...]:
        return (
            DEFAULT_PROJECT_NAME,
            ".gitignore",
            "pyproject.toml",
            "README.md",
            "tests",
        ) + self.extra_files

    @property
    @abc.abstractmethod
    def pyproject_toml_lines(self) -> tuple[str, ...]:
        ...

    @property
    def lint_output(self) -> tuple[str, ...]:  # TODO
        return (
            self.install("lint"),
            f"{self.runner}flake8 {DEFAULT_PROJECT_NAME} tests",
            "files would be left unchanged",
            f"{self.runner}black --check --diff {ALL_SOURCE}",
            f"{self.runner}pylint {DEFAULT_PROJECT_NAME} tests",
            "Your code has been rated at 10.00/10",
            f"{self.runner}isort --check-only {ALL_SOURCE}",
            f"{self.runner}mypy {ALL_SOURCE}",
        )

    @property
    def test_output(self) -> tuple[str, ...]:
        return (
            self.install("test"),
            "test session starts",
            "files skipped due to complete coverage.",
        )

    @property
    def cleaned_up_file_parts(self) -> tuple[str, ...]:
        return (
            ".coverage",
            ".pytest_cache",
            ".mypy_cache",
            f"{DEFAULT_PROJECT_NAME}.egg-info",
            "pip-wheel-metadata",
            ".pyc",
            ".pyo",
            "__pycache__",
            "build",
            "dist",
            ".tar.gz",
            ".whl",
        )

    @property
    def format_output(self) -> tuple[str, ...]:  # TODO
        return (
            self.install("lint"),
            f"{self.runner}black {ALL_SOURCE}",
            "files left unchanged",
            f"{self.runner}isort {ALL_SOURCE}",
        )

    @property
    def build_patterns(self) -> tuple[str, ...]:
        return ("./dist/*.tar.gz", "./dist/*.whl")


class TestPoetryProjectCreation(Context):
    @property
    def pyproject_toml_lines(self) -> tuple[str, ...]:
        return ("[tool.poetry]",)

    @property
    def extra_files(self) -> tuple[str, ...]:
        return ("poetry.lock",)

    @property
    def runner(self) -> str:
        return "poetry run "

    def install(self, extra: str) -> str:
        return f"poetry install --with {extra}"

    def test_project_creation(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            assert_successful_creation(result)
            assert_expected_files_exist(result, files=self.project_files)
            assert_project_file_contains(
                result, "pyproject.toml", self.pyproject_toml_lines
            )

    def test_project_creation_with_invalid_name_fails(
        self,
        cookies: Cookies,
    ) -> None:
        result = cookies.bake(extra_context={"package_name": "Foo-Bar"})
        assert result.exit_code != 0

    def test_linting(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            output = check_output_in_result_dir("make lint", result)
            assert_expected_lines_are_in_output(self.lint_output, output)

    def test_test_run(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            output = check_output_in_result_dir("make test", result)
            assert_expected_lines_are_in_output(self.test_output, output)

    def test_cleaning(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            check_output_in_result_dir("make lint", result)
            check_output_in_result_dir("make test", result)
            check_output_in_result_dir("make build", result)
            check_output_in_result_dir("make clean", result)

            assert_expected_files_do_not_exist(
                result,
                files=self.cleaned_up_file_parts,
            )

    def test_clean_in_empty_project_dir(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            check_output_in_result_dir("make clean", result)

    def test_formatting(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            output = check_output_in_result_dir("make format", result)
            assert_expected_lines_are_in_output(self.format_output, output)

    def test_build(self, cookies: Cookies) -> None:
        with generate_temporary_project(cookies) as result:
            check_output_in_result_dir("make build", result)
            with inside_directory_of(result):
                for pattern in self.build_patterns:
                    assert glob.glob(pattern)
