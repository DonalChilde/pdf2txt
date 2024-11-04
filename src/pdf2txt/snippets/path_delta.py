from pathlib import Path


def path_delta(
    source_base_path: Path, source_sub_path: Path, destination_base_path: Path
) -> Path:
    """
    Recreate sub path structure of a source dir in a destination dir.

    Base paths should be directories, and the sub path can be a directory or file.
    """
    destination_sub_path = destination_base_path / source_sub_path.relative_to(
        source_base_path
    )
    return destination_sub_path
