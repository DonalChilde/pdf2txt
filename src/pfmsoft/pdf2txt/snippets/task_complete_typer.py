"""task_complete.py."""

from time import perf_counter_ns

import typer


def task_complete(ctx: typer.Context, app_name: str):
    """Assuming the ctx.obj is a dict with [app_name][start_perf] defined, output a task completed message."""
    app_data = ctx.obj.get(app_name, None)
    if app_data is None:
        return
    start_time = app_data.get("start_perf", None)
    if start_time is None:
        return
    end_time = perf_counter_ns()
    length = end_time - start_time
    typer.echo(f"\nTask completed in {length/1000000000:9f} seconds.")
