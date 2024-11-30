"""Pytest conftest file."""

import logging
from collections.abc import Iterable
from pathlib import Path

import pytest
from typer.testing import CliRunner

logger = logging.getLogger(__name__)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking Typer command-line interfaces."""
    return CliRunner()


@pytest.fixture(scope="session", name="test_output_dir")
def test_output_dir_(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Make a temp directory for output data."""
    test_output_dir = tmp_path_factory.mktemp("pfmsoft-pdf2txt")
    logger.info(f"Designated {test_output_dir} as the test output directory.")
    return test_output_dir


########################################################################
# Add an option to mark slow tests, so that they don't run every time. #
########################################################################
def pytest_addoption(parser: pytest.Parser):
    """Add a command line option to pytest."""
    # https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    # conftest.py must be in the root test package.
    logger.info("Added --runslow cli option to pytest.")
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config: pytest.Config):
    """Add a `slow` mark that can be used on pytest tests.

    This will cause tests marked as slow to be skipped,
    unless the --runslow cli option is given to pytest.

    Example:
        ```python
        import pytest


        @pytest.mark.slow
        def test_example():
            value = 5
            assert value > 1
        ```
    """
    logger.info("Added `slow` test mark.")
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config: pytest.Config, items: Iterable[pytest.Item]):
    """Skips tests marked as `slow`, unless --runslow is given as a cli option to pytest."""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            logger.info(f"Test: {item.name} marked as slow. Skipping test.")
            item.add_marker(skip_slow)
