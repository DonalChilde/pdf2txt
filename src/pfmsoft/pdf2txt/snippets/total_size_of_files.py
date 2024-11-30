"""total_size_of_files.py."""

from collections.abc import Iterable
from pathlib import Path


def total_size_of_files(file_paths: Iterable[Path]) -> int:
    """Return the total size of an Iterable of file paths."""
    total = 0
    for file_path in file_paths:
        total += file_path.stat().st_size
    return total
