"""
    _summary_

    _extended_summary_
"""


def sizeof_fmt(num, suffix="B"):
    """
    _summary_

    _extended_summary_

    Args:
        num: _description_
        suffix: _description_. Defaults to "B".

    Returns:
        _description_
    from https://stackoverflow.com/a/1094933
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
