"""The main callback function."""

import logging
from datetime import UTC, datetime
from os import cpu_count
from pathlib import Path
from time import perf_counter_ns
from typing import Annotated, TypedDict

import typer

from pfmsoft.pdf2txt import APP_DIR, APP_NAME, LOG_DIR

logger = logging.getLogger(__name__)
CPU_COUNT = cpu_count()


class AppData(TypedDict):
    """App data to be stored on ctx."""

    app_name: str
    log_dir: Path
    app_dir: Path
    start_perf: int
    start_time: datetime
    debug: bool
    verbosity: int
    processors: int


def base_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[
        int, typer.Option("-v", help="Verbosity. eg. -vvv", count=True)
    ] = 1,
    processors: Annotated[
        int,
        typer.Option("-p", help=f"The number of processors to use. max={CPU_COUNT}."),
    ] = 1,
):
    """Describe what your app does here."""
    if CPU_COUNT is None:
        processors = 1
    elif processors > CPU_COUNT:
        processors = CPU_COUNT
    app_data = AppData(
        app_name=APP_NAME,
        log_dir=LOG_DIR,
        app_dir=APP_DIR,
        start_perf=perf_counter_ns(),
        start_time=datetime.now(UTC),
        debug=debug,
        verbosity=verbosity,
        processors=processors,
    )
    typer.echo(f"Welcome to {APP_NAME}!")
    # typer.echo(f"{APP_NAME}'s application directory is {APP_DIR}")
    typer.echo(f"{APP_NAME}'s log directory is {LOG_DIR}")
    ctx.ensure_object(dict)
    ctx.obj[APP_NAME] = app_data
    logger.info(f"{APP_NAME} started with {app_data!r}")

    if ctx.obj[APP_NAME]["verbosity"] >= 3:
        typer.echo(f"Verbosity: {ctx.obj[APP_NAME]["verbosity"]}")
        typer.echo(f"Debug: {ctx.obj[APP_NAME]["debug"]}")
        formatted_time = ctx.obj[APP_NAME]["start_time"].strftime(
            "%Y-%m-%d %H:%M:%S.%fZ"
        )
        typer.echo(f"Started at: {formatted_time}")
        typer.echo(f"{f"start_perf={ctx.obj[APP_NAME]['start_perf']}"}")
        typer.echo(
            f"Number of processors used={ctx.obj[APP_NAME]['processors']}/{CPU_COUNT}"
        )
