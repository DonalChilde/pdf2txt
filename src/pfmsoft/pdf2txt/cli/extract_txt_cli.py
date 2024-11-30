"""Command-line interface."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

from pfmsoft.pdf2txt.extract_txt import extract_text_from_pdf_to_file
from pfmsoft.pdf2txt.snippets.path_delta import path_delta

# TODO support extracting text to command line - pipe.


app = typer.Typer()


@dataclass
class ExtractJob:
    """Job to extract text from a pdf."""

    path_in: Path
    path_out: Path
    overwrite: bool = False
    halt_on_fail: bool = False


def total_size_of_files(jobs: Sequence[ExtractJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


@app.command()
def text(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source pdf file.", exists=True, dir_okay=False, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text file.")
    ],
    file_name: Annotated[
        Path | None,
        typer.Option(help="file name for output if differrent from default."),
    ] = None,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Extract text from a single pdf file."""
    in_suffix = path_in.suffix.lower()
    if in_suffix != ".pdf":
        typer.echo(
            f"input file might not be a pdf, suffix for {path_in.name} is not "
            f"'.pdf' (case insensitive)."
        )
    if file_name:
        path_out = path_out / Path(file_name.name)
    else:
        path_out = path_out / Path(path_in.name).with_suffix(".txt")
    job = ExtractJob(
        path_in=path_in, path_out=path_out, overwrite=overwrite, halt_on_fail=False
    )
    jobs = [job]

    extract_txt_rich(jobs=jobs)


def extract_txt_rich(
    jobs: Sequence[ExtractJob],
):
    """Extract text from pdf files, show rich text progress bar."""
    file_count = len(jobs)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            f"1 of {file_count}", total=total_size_of_files(jobs=jobs)
        )
        for idx, job in enumerate(jobs, start=1):
            try:
                extract_text_from_pdf_to_file(job.path_in, job.path_out, job.overwrite)
                progress.update(
                    task,
                    advance=job.path_in.stat().st_size,
                    description=f"{idx} of {file_count}",
                )
            except Exception as e:
                if job.halt_on_fail:
                    raise e
                progress.console.print(f"Skipping {job}\n\tCause: {e}")
                progress.update(
                    task,
                    advance=job.path_in.stat().st_size,
                    description=f"{idx} of {file_count}",
                )


@app.command()
def all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source directory for files ending in .pdf, case insensitive.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text files.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    recurse: Annotated[
        bool, typer.Option(help="Also extract text from sub directories of path_in,")
    ] = False,
    halt_on_fail: Annotated[
        bool, typer.Option(help="Exit program if any one task fails.")
    ] = False,
):
    """Extract multiple files, with optional recursion, and automatic naming of extracted files.

    If recursing sub directories, the sub directory structure is reproduced
    in the output directory. Automatic file renaming will replace the .pdf suffix
    with the .txt suffix.
    """
    _ = ctx
    jobs = build_jobs_from_directory(
        path_in=path_in,
        path_out=path_out,
        recurse=recurse,
        overwrite=overwrite,
        halt_on_fail=halt_on_fail,
    )
    extract_txt_rich(jobs=jobs)


def build_jobs_from_directory(
    path_in: Path, path_out: Path, recurse: bool, overwrite: bool, halt_on_fail: bool
) -> list[ExtractJob]:
    """Build extract jobs based on pdf files foud in a directory.

    _extended_summary_

    Args:
        path_in (_type_): _description_
        path_out (_type_): _description_
        recurse (_type_): _description_
        overwrite (_type_): _description_
        halt_on_fail (_type_): _description_

    Raises:
        typer.BadParameter: _description_
        typer.BadParameter: _description_

    Returns:
        list[ExtractJob]: The jobs.
    """
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
    jobs: list[ExtractJob] = []
    for input_file in input_files:
        job = ExtractJob(
            path_in=input_file,
            path_out=path_delta(
                source_base_path=path_in,
                source_sub_path=input_file,
                destination_base_path=path_out,
            ),
            overwrite=overwrite,
            halt_on_fail=halt_on_fail,
        )
        job.path_out = job.path_out.with_suffix(".txt")
        jobs.append(job)
    return jobs


if __name__ == "__main__":
    app()
