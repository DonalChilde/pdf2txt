"""Command-line interface."""

from pathlib import Path

import typer
from pfmsoft.snippets.file.validate_file_out import validate_file_out
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def extract(
    path_in: Annotated[Path, typer.Argument(help="source pdf file.")],
    path_out: Annotated[Path, typer.Argument(help="destination text file.")],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """
    Extract text from a pdf file.
    """
    if not path_in.is_file():
        print(f"{path_in} is not a file.")
        raise typer.Exit(code=1)
    if path_in.suffix.lower() is not "pdf":
        print(f"input file might not be a pdf, suffix for {path_in.name} is not 'pdf'.")
        raise typer.Exit(code=1)
    if path_out.is_dir():
        print(f"{path_out} is a directory, and must point to a file.")
    if path_out.is_file() and not overwrite:
        print(f"{path_out} exists and overwrite was not selected.")
    if not validate_file_out(path_out, overwrite=overwrite, ensure_parent=True):
        print(f"Unable to create path to {path_out}. is it writable?")
        raise typer.Exit(code=1)
    print(path_in, path_out, overwrite)


@app.command()
def extract_all(
    path_in: Annotated[
        Path, typer.Argument(help="source directory containing pdf files.")
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text files.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    recurse: Annotated[
        bool, typer.Option(help="extract text from sub directories of path_in,")
    ] = False,
):
    """
    Extract multiple files, with optional recursion
    """
    print(path_in, path_out, overwrite, recurse)


if __name__ == "__main__":
    app()
