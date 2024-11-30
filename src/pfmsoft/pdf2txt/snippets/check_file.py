"""check_file.py."""

from pathlib import Path


def check_file(path_out: Path, ensure_parents: bool, overwrite: bool = False) -> bool:
    """Check that path is valid for file output.

    Checks that path is not an existing directory.
    Checks if overwrite is allowed for existing files.
    """
    if path_out.exists():
        if path_out.is_dir():
            raise ValueError(f"Output path exists and it is a directory. {path_out}")
        if path_out.is_file():
            if not overwrite:
                raise ValueError(
                    f"Output path exists and overwrite is false. {path_out}"
                )
    if ensure_parents:
        path_out.parent.mkdir(parents=True, exist_ok=True)
    return True
