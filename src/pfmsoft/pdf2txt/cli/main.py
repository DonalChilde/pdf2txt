"""Command-line interface."""

from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter_ns
from typing import Iterable, List

import typer
from typing_extensions import Annotated

from pfmsoft.pdf2txt.extract import extract_text_from_pdf_to_file
from pfmsoft.pdf2txt.snippets.path_delta import path_delta
from pfmsoft.pdf2txt.snippets.sizeof_fmt import sizeof_fmt
from pfmsoft.pdf2txt.snippets.task_complete_typer import task_complete
from rich.progress import (
    Progress,
    TotalFileSizeColumn,
    TimeElapsedColumn,
    FileSizeColumn,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
)


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


@dataclass
class ExtractJob:
    path_in: Path
    path_out: Path
    overwrite: bool = False
    halt_on_fail: bool = False


@dataclass
class ExtractJobs:
    jobs: List[ExtractJob] = field(default_factory=list)

    def total_size_of_files(self) -> int:
        total = 0
        for job in self.jobs:
            total += job.path_in.stat().st_size
        return total


@app.command()
def extract(
    ctx: typer.Context,
    path_in: Annotated[
        Path, typer.Argument(help="source pdf file.", exists=True, dir_okay=False)
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
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    """
    Extract text from a single pdf file.
    """
    if not path_in.is_file():
        print(f"{path_in} is not a file.")
        raise typer.BadParameter(f"PATH_IN: {path_in} is not a file.")
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
    jobs = [
        job,
    ]
    extract_jobs = ExtractJobs(jobs=jobs)
    try:
        extract_txt_rich(jobs=extract_jobs, suppress_status_msgs=suppress_status_msgs)
    except Exception as e:
        print(e)
        raise typer.Exit(code=1)
    if not suppress_status_msgs:
        task_complete(ctx)


def extract_txt_rich(
    jobs: ExtractJobs,
    suppress_status_msgs: bool = False,
):
    file_count = len(jobs.jobs)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"1 of {file_count}", total=jobs.total_size_of_files())
        for idx, job in enumerate(jobs.jobs, start=1):
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
                continue


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
    jobs: List[ExtractJob] = []
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
    extract_jobs = ExtractJobs(jobs=jobs)
    try:
        extract_txt_rich(jobs=extract_jobs, suppress_status_msgs=suppress_status_msgs)
    except Exception as e:
        # TODO log this instead of print
        print(f"{locals()!r}")
        raise typer.BadParameter(str(e))

    task_complete(ctx)


def file_stat_msg(file_path: Path) -> str:
    return f"{file_path.name} - {sizeof_fmt(file_path.stat().st_size)}"


def total_size_of_files(file_paths: Iterable[Path]) -> int:
    total = 0
    for file_path in file_paths:
        total += file_path.stat().st_size
    return total


if __name__ == "__main__":
    app()
