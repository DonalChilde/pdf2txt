from importlib import resources
from pathlib import Path

from tests.resources import RESOURCES_ANCHOR
from typer.testing import CliRunner

from pdf2txt.pdf2txt_cli import app

DATA_FILE_NAME = "PBS_LGA_November_2024_20241010125956.pdf"
DATA_FILE_PATH = "pdf/2024_11_LGA"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_extract_pdf(runner: CliRunner, test_output_dir: Path):
    """"""
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    output_path = test_output_dir.joinpath(Path("2024_11_LGA/extract"), DATA_FILE_NAME)
    output_path = output_path.with_suffix(".txt")
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(
            app, ["-vvv", "extract", str(input_path), str(output_path)]
        )
        assert "Verbosity: 3" in result.stdout
        print(result.stdout)
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
    # assert False
