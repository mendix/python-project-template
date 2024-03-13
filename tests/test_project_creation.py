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
import dataclasses
import glob
from collections.abc import Collection

import pytest
from pytest_cookies.plugin import Cookies, Result

from .util import (
    check_output_in_result_dir,
    inside_directory_of,
)

DEFAULT_PROJECT_NAME = "pymx"
ALL_SOURCE = f"{DEFAULT_PROJECT_NAME} tests"


def assert_successful_creation(result: Result) -> None:
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    assert result.exception is None


def assert_expected_files_exist(
    result: Result,
    files: Collection[str],
) -> None:
    created_files = [f.name for f in result.project_path.iterdir()]
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
            content: str = fobj.read()
            for line in expected_lines:
                assert f"{line}" in content


class BaseContext(abc.ABC):
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
    @abc.abstractmethod
    def file_lines(self) -> dict[str, tuple[str, ...]]:
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
    def lint_output(self) -> tuple[str, ...]:
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
    def format_output(self) -> tuple[str, ...]:
        return (
            self.install("lint"),
            f"{self.runner}black {ALL_SOURCE}",
            "files left unchanged",
            f"{self.runner}isort {ALL_SOURCE}",
        )

    @property
    def build_patterns(self) -> tuple[str, ...]:
        return ("./dist/*.tar.gz", "./dist/*.whl")

    @property
    def context(self) -> dict[str, str]:
        return {}


class PoetryProjectContext(BaseContext):
    @property
    def file_lines(self) -> dict[str, tuple[str, ...]]:
        return {
            "pyproject.toml": (
                "[tool.poetry]",
                'build-backend = "poetry.core.masonry.api"',
                # Black
                "line-length = 79",
                # Isort
                "line_length = 79",
                # Pylint
                "max-line-length = 79",
            ),
            "Makefile": (
                "$(POETRY) run",
                "$(POETRY) install",
            ),
        }

    @property
    def extra_files(self) -> tuple[str, ...]:
        return ("poetry.lock",)

    @property
    def runner(self) -> str:
        return "poetry run "

    def install(self, extra: str) -> str:
        return f"poetry install --with {extra}"


class SetupToolsProjectContext(BaseContext):
    @property
    def context(self) -> dict[str, str]:
        return {"build_system": "setuptools"}

    @property
    def file_lines(self) -> dict[str, tuple[str, ...]]:
        return {
            "pyproject.toml": (
                "[project]",
                'build-backend = "setuptools.build_meta"',
                # Black
                "line-length = 79",
                # Isort
                "line_length = 79",
                # Pylint
                "max-line-length = 79",
            ),
            "Makefile": ("$(PIP) install",),
        }

    @property
    def runner(self) -> str:
        return ""

    def install(self, extra: str) -> str:
        return f"pip3 install -e .[{extra}]"


@dataclasses.dataclass
class Project:
    ctx: BaseContext
    result: Result


@pytest.fixture(scope="function", name="project")
def project_fixture(
    cookies: Cookies, request: pytest.FixtureRequest
) -> Project:
    context: BaseContext = request.param
    result = cookies.bake(extra_context=context.context)
    return Project(context, result)


@pytest.mark.parametrize(
    ("context",),
    (
        (PoetryProjectContext(),),
        (SetupToolsProjectContext(),),
    ),
)
class TestFailedProjectCreation:
    def test_project_creation_with_invalid_name_fails(
        self,
        cookies: Cookies,
        context: BaseContext,
    ) -> None:
        extra_context = context.context
        extra_context |= {"package_name": "Foo-Bar"}
        result = cookies.bake(extra_context=extra_context)
        assert result.exit_code != 0

    def test_project_creation_with_invalid_line_length_fails(
        self,
        cookies: Cookies,
        context: BaseContext,
    ) -> None:
        extra_context = context.context
        extra_context |= {"line_length": "78"}
        result = cookies.bake(extra_context=extra_context)
        assert result.exit_code != 0


@pytest.mark.parametrize(
    ("project",),
    (
        (PoetryProjectContext(),),
        (SetupToolsProjectContext(),),
    ),
    indirect=True,
)
class TestProjectCreation:
    def test_project_creation(self, project: Project) -> None:
        assert_successful_creation(project.result)
        assert_expected_files_exist(
            project.result, files=project.ctx.project_files
        )
        for filename, lines in project.ctx.file_lines.items():
            assert_project_file_contains(project.result, filename, lines)

    def test_linting(self, project: Project) -> None:
        output = check_output_in_result_dir("make lint", project.result)
        assert_expected_lines_are_in_output(project.ctx.lint_output, output)

    def test_test_run(self, project: Project) -> None:
        output = check_output_in_result_dir("make test", project.result)
        assert_expected_lines_are_in_output(project.ctx.test_output, output)

    def test_cleaning(self, project: Project) -> None:
        check_output_in_result_dir("make lint", project.result)
        check_output_in_result_dir("make test", project.result)
        check_output_in_result_dir("make build", project.result)
        check_output_in_result_dir("make clean", project.result)

        assert_expected_files_do_not_exist(
            project.result,
            files=project.ctx.cleaned_up_file_parts,
        )

    def test_clean_in_empty_project_dir(self, project: Project) -> None:
        check_output_in_result_dir("make clean", project.result)

    def test_formatting(self, project: Project) -> None:
        output = check_output_in_result_dir("make format", project.result)
        assert_expected_lines_are_in_output(project.ctx.format_output, output)

    def test_build(self, project: Project) -> None:
        check_output_in_result_dir("make build", project.result)
        with inside_directory_of(project.result):
            for pattern in project.ctx.build_patterns:
                assert glob.glob(pattern)
