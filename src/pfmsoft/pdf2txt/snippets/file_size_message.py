"""file_size_message.py."""

from pathlib import Path

from .sizeof_fmt import sizeof_fmt


def file_size_msg(file_path: Path) -> str:
    """Returns a string of [filename] - [file size]."""
    return f"{file_path.name} - {sizeof_fmt(file_path.stat().st_size)}"
