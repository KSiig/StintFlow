"""Timestamp helpers.

Small utility to convert a seconds value to an ``HH:MM:SS`` string. The
function accepts integers, floats or numeric strings and clamps negative
values to zero.
"""

from typing import Any


def _seconds_to_hhmmss(seconds: int | float | str) -> str:
    """Convert ``seconds`` to an ``HH:MM:SS`` string.

    Args:
        seconds: total seconds as an int, float or numeric string. Non-numeric
            inputs raise a ``ValueError``.

    Returns:
        A zero-padded time string (e.g. "01:05:09").
    """
    try:
        total = int(float(seconds))
    except Exception as exc:
        raise ValueError(f"Invalid seconds value: {seconds!r}") from exc

    total = max(0, total)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02}:{m:02}:{s:02}"