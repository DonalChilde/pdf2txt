from time import perf_counter_ns

import typer


def task_complete(ctx: typer.Context):
    """Assuming the ctx.obj is a dict with START_TIME defined, output a task completed message."""
    start_time = ctx.obj.get("START_TIME", None)
    if start_time is not None:
        end_time = perf_counter_ns()
        length = end_time - start_time
        typer.echo(f"\nTask completed in {length/1000000000:9f} seconds.")
