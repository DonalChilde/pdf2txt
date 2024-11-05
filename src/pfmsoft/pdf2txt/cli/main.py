"""Command-line interface."""

from pathlib import Path
from time import perf_counter_ns

import typer
from typing_extensions import Annotated

from pfmsoft.pdf2txt.extract import extract_text_from_pdf_to_file
from pfmsoft.pdf2txt.snippets.path_delta import path_delta
from pfmsoft.pdf2txt.snippets.sizeof_fmt import sizeof_fmt
from pfmsoft.pdf2txt.snippets.task_complete_typer import task_complete

# TODO support extracting text to command line - pipe.


def default_options(
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


app = typer.Typer(callback=default_options)


@app.command()
def extract(
    ctx: typer.Context,
    path_in: Annotated[
        Path, typer.Argument(help="source pdf file.", exists=True, dir_okay=False)
    ],
    path_out: Annotated[Path, typer.Argument(help="destination text file.")],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    """
    Extract text from a single pdf file.
    """
    try:
        extract_txt(
            ctx=ctx,
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
            suppress_status_msgs=suppress_status_msgs,
        )
    except Exception as e:
        print(e)
        raise typer.Exit(code=1)
    if not suppress_status_msgs:
        task_complete(ctx)


def extract_txt(
    ctx: typer.Context,
    path_in: Path,
    path_out: Path,
    overwrite: bool = False,
    suppress_status_msgs: bool = False,
):
    _ = ctx
    if not path_in.is_file():
        print(f"{path_in} is not a file.")
        raise typer.BadParameter(f"PATH_IN: {path_in} is not a file.")
    in_suffix = path_in.suffix.lower()
    if in_suffix != ".pdf":
        typer.echo(
            f"input file might not be a pdf, suffix for {path_in.name} is not "
            f"'.pdf' (case insensitive)."
        )
    job_message = f"Extracting text from {file_stat_msg(path_in)} to {path_out}"
    if not suppress_status_msgs:
        typer.echo(job_message)

    extract_text_from_pdf_to_file(path_in, path_out, overwrite)


@app.command()
def extract_all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source directory for files ending in .pdf, case insensitive.",
            exists=True,
            file_okay=False,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text files.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
    recurse: Annotated[
        bool, typer.Option(help="extract text from sub directories of path_in,")
    ] = False,
    halt_on_fail: Annotated[
        bool, typer.Option(help="Exit program if any one task fails.")
    ] = False,
):
    """
    Extract multiple files, with optional recursion, and automatic naming of extracted files.

    If recursing sub directories, the sub directory structure is reproduced
    in the output directory. Automatic file renaming will replace the .pdf suffix
    with the .txt suffix.
    """
    try:
        extract_txt_from_all(
            ctx=ctx,
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
            suppress_status_msgs=suppress_status_msgs,
            recurse=recurse,
            halt_on_fail=halt_on_fail,
        )
    except Exception as e:
        # TODO log this instead of print
        print(f"{locals()!r}")
        raise typer.BadParameter(str(e))

    task_complete(ctx)


def extract_txt_from_all(
    ctx: typer.Context,
    path_in: Path,
    path_out: Path,
    overwrite: bool = False,
    suppress_status_msgs: bool = False,
    recurse: bool = False,
    halt_on_fail: bool = False,
):
    if path_out.is_file():
        raise typer.BadParameter(
            f"PATH_OUT: {path_out} is an existing file, not a directory."
        )
    if recurse:
        input_files = list(path_in.glob("**/*.pdf", case_sensitive=False))
    else:
        input_files = list(path_in.glob("*.pdf", case_sensitive=False))
    if not input_files:
        raise typer.BadParameter(f"No pdf files were found in {path_in}")
    file_count = len(input_files)
    for idx, file in enumerate(input_files, start=1):
        typer.echo(f"Task {idx} of {file_count}")
        output_path = path_delta(
            source_base_path=path_in,
            source_sub_path=file,
            destination_base_path=path_out,
        )
        output_path = output_path.with_suffix(".txt")
        try:
            extract_txt(
                ctx=ctx,
                path_in=file,
                path_out=output_path,
                overwrite=overwrite,
                suppress_status_msgs=suppress_status_msgs,
            )
        except Exception as e:
            if halt_on_fail:
                raise e
            typer.echo(f"Skipping {file}\n\tCause: {e}")
            continue


def file_stat_msg(file_path: Path) -> str:
    return f"{file_path.name} - {sizeof_fmt(file_path.stat().st_size)}"


if __name__ == "__main__":
    app()
