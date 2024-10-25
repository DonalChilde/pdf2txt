"""Test cases for the console module."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pdf2txt.pdf2txt_cli import app


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_extract(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["extract", "/tmp", "/tmp"])
    print(result.stdout)
    assert result.exit_code == 0
