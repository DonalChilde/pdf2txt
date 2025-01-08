"""test_extract_txt."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pfmsoft.pdf2txt.cli.main_typer import app
from tests.resources import RESOURCES_ANCHOR
from tests.resources.pdf import PDF_ANCHOR

DATA_FILE_NAME = "sample.pdf"


def test_extract_pdf(runner: CliRunner, test_output_dir: Path):
    """Test extracting text from a pdf file via the cli."""
    file_resource = resources.files(PDF_ANCHOR).joinpath(DATA_FILE_NAME)
    with resources.as_file(file_resource) as input_path:
        output_file = Path(input_path.name).with_suffix(".txt")
        output_dir = test_output_dir / "extract_from_file"
        output_path = output_dir / output_file

        result = runner.invoke(
            app, ["-vvv", "extract", str(input_path), str(output_dir)]
        )
        assert "Verbosity: 3" in result.stdout
        print(result.stdout)
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
        assert output_path.is_file()
        text = output_path.read_text()
        assert "Ipsum" in text
