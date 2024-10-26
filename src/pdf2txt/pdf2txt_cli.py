"""Command-line interface."""

from pathlib import Path
from time import perf_counter_ns

import typer
from typing_extensions import Annotated

from pdf2txt.extract import extract_text_from_pdf_to_file
from pdf2txt.snippets.sizeof_fmt import sizeof_fmt
from pdf2txt.snippets.task_complete_typer import task_complete

app = typer.Typer()


# TODO support extracting text to command line - pipe.


@app.callback()
def cli(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Extract text from pdf files."""

    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    typer.echo(f"Verbosity: {verbosity}")
    ctx.obj["VERBOSITY"] = verbosity


@app.command()
def extract(
    ctx: typer.Context,
    path_in: Annotated[Path, typer.Argument(help="source pdf file.")],
    path_out: Annotated[Path, typer.Argument(help="destination text file.")],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress job status messages.")
    ] = False,
):
    """
    Extract text from a pdf file.
    """
    # TODO log this instead of print
    # print(f"{locals()!r}")
    if ctx.obj["VERBOSITY"] == 0:
        suppress_status_msgs = True
    if not path_in.is_file():
        print(f"{path_in} is not a file.")
        raise typer.Exit(code=1)
    in_suffix = path_in.suffix.lower()
    if in_suffix != ".pdf":
        print(
            f"input file might not be a pdf, suffix for {path_in.name} is not "
            f"'.pdf', it is {in_suffix}."
        )
    job_message = f"Extracting text from {file_stat_msg(path_in)} to {path_out}"
    if not suppress_status_msgs:
        typer.echo(job_message)
    try:
        extract_text_from_pdf_to_file(path_in, path_out, overwrite)
    except ValueError as e:
        print(e)
        raise typer.Exit(code=1)
    if not suppress_status_msgs:
        task_complete(ctx)

    # assert False


@app.command()
def extract_all(
    ctx: typer.Context,
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
    Extract multiple files, with optional recursion, and automatic naming of extracted files.

    If recursing sub directories, the sub directory structure is reproduced
    in the output directory. Automatic file renaming will replace the .pdf suffix
    with the .txt suffix.
    """
    # TODO log this instead of print
    print(f"{locals()!r}")
    task_complete(ctx)


def file_stat_msg(file_path: Path) -> str:
    return f"{file_path.name} - {sizeof_fmt(file_path.stat().st_size)}"


if __name__ == "__main__":
    app()
