"""Test cases for the console module."""

from typer.testing import CliRunner

from pdf2txt.pdf2txt_cli import app


def test_app(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_extract(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["extract", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_extract_all(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["extract-all", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
