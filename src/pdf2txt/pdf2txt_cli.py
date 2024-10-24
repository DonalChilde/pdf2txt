"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Pdf2Txt."""


if __name__ == "__main__":
    main(prog_name="pdf2txt")  # pragma: no cover
