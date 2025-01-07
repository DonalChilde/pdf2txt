"""FILE: extract.py."""

import multiprocessing
import random
from collections.abc import Iterable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing.managers import DictProxy
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

from pfmsoft.pdf2txt import APP_NAME
from pfmsoft.pdf2txt.extract_txt import extract_text_from_pdf_to_file
from pfmsoft.pdf2txt.snippets.path_delta import path_delta

# TODO support extracting text to command line - pipe.

progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    FileSizeColumn(),
    TotalFileSizeColumn(),
    TimeElapsedColumn(),
)


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
def extract(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source pdf file or a directory containing pdf files.",
            exists=True,
            dir_okay=True,
            file_okay=True,
        ),
    ],
    path_out: Annotated[Path, typer.Argument(help="Path to the output directory.")],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    file_name: Annotated[
        str | None,
        typer.Option(
            "-f",
            help="An optional file name to use instead of the default. Only valid during single file output.",
        ),
    ] = None,
    halt_on_fail: Annotated[
        bool, typer.Option(help="Exit program if any one task fails.")
    ] = False,
):
    """Extract text from pdf files."""
    if path_out.exists():
        if not path_out.is_dir():
            raise typer.BadParameter(f"PATH_OUT should be a directory. {path_out=}")

    jobs: list[ExtractJob] = []

    if path_in.is_file():
        if path_in.suffix.lower() != ".pdf":
            typer.echo(
                f"input file might not be a pdf, suffix for {path_in.name} is not "
                f"'.pdf' (case insensitive)."
            )
        job = build_one(
            path_in=path_in,
            path_out=path_out,
            file_name=file_name,
            overwrite=overwrite,
            halt_on_fail=halt_on_fail,
        )
        jobs.append(job)

    if path_in.is_dir():
        for job in build_many(
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
            halt_on_fail=halt_on_fail,
        ):
            jobs.append(job)
    processors: int = ctx.obj[APP_NAME]["processors"]
    if processors == 1:
        extract_txt_rich(jobs=jobs)
    elif processors > 1:
        extract_txt_multiprocessing(jobs=jobs, processors=processors)
    else:
        raise typer.BadParameter(f"Received a bad value for processors. {processors=}")


def build_many(
    path_in: Path,
    path_out: Path,
    overwrite: bool,
    halt_on_fail: bool,
) -> Iterable[ExtractJob]:
    for file in path_in.glob(".pdf", case_sensitive=False):
        file_out = path_out / path_in.name
        file_out.with_suffix(".txt")
        job = ExtractJob(
            path_in=file,
            path_out=file_out,
            overwrite=overwrite,
            halt_on_fail=halt_on_fail,
        )
        yield job


def build_one(
    path_in: Path,
    path_out: Path,
    file_name: str | None,
    overwrite: bool,
    halt_on_fail: bool,
) -> ExtractJob:
    if file_name is None:
        file_out = path_out / path_in.name
        file_out.with_suffix(".txt")
    else:
        file_out = path_out / file_name
    return ExtractJob(
        path_in=path_in,
        path_out=file_out,
        overwrite=overwrite,
        halt_on_fail=halt_on_fail,
    )


def extract_txt_multiprocessing(jobs: Sequence[ExtractJob], processors: int):
    file_count = len(jobs)
    skipped = 0
    with progress:
        monitor_task = progress.add_task(
            f"Extracting 1 of {file_count}. { f" {skipped} files skipped." if skipped>0 else None}",
            total=total_size_of_files(jobs=jobs),
        )
        futures = []
        with multiprocessing.Manager() as manager:
            shared = manager.dict()
            shared["skipped"] = 0
            with ProcessPoolExecutor(max_workers=processors) as executor:
                for idx, job in enumerate(jobs, start=1):
                    futures.append(executor.submit(work, idx, job, shared))
                while (n_finished := sum([future.done() for future in futures])) < len(
                    futures
                ):
                    completed = 0
                    for job_id, job_info in shared.items():
                        completed += job_info["job_size"]
                    skipped = shared["skipped"]
                    progress.update(
                        monitor_task,
                        description=f"Extracting {idx} of {file_count}. { f" {skipped} files skipped." if skipped>0 else None}",
                        completed=completed,
                    )


def work(idx: int, job: ExtractJob, shared: DictProxy[Any, Any]):
    try:
        extract_text_from_pdf_to_file(job.path_in, job.path_out, job.overwrite)
        shared[idx]["job_size"] = job.path_in.stat().st_size
    except Exception as e:
        if job.halt_on_fail:
            raise e
        progress.console.print(f"Skipping {job}\n\tCause: {e}")
        shared["skipped"] += 1


def extract_txt_rich(
    jobs: Sequence[ExtractJob],
):
    """Extract text from pdf files, show rich text progress bar."""
    file_count = len(jobs)
    skipped = 0
    with progress:
        monitor_task = progress.add_task(
            f"Extracting 1 of {file_count}. { f" {skipped} files skipped." if skipped>0 else None}",
            total=total_size_of_files(jobs=jobs),
        )
        for idx, job in enumerate(jobs, start=1):
            try:
                extract_text_from_pdf_to_file(job.path_in, job.path_out, job.overwrite)
                progress.update(
                    monitor_task,
                    advance=job.path_in.stat().st_size,
                    description=f"Extracting {idx} of {file_count}. { f" {skipped} files skipped." if skipped>0 else None}",
                )
            except Exception as e:
                if job.halt_on_fail:
                    raise e
                progress.console.print(f"Skipping {job}\n\tCause: {e}")
                progress.update(
                    monitor_task,
                    advance=job.path_in.stat().st_size,
                    description=f"{idx} of {file_count}",
                )
