"""Small helper to determine whether a tyre wear value represents a new tyre.

One function per file is a project convention; this module purposefully
contains a single, well-documented function used by the tyre-management
helpers elsewhere in the tracker.
"""

from .constants import WEAR_COMPARISON_EPSILON


def _is_new_tire(wear: float | str | None) -> bool:
    """Return True when `wear` indicates a new tyre.

    Args:
        wear: numeric wear (0.0..1.0), a numeric string, or None.

    Returns:
        True when the wear is close enough to 1.0 to be considered new.
        Non-numeric or missing values return False.
    """
    if wear is None:
        return False

    try:
        w = float(wear)
    except (TypeError, ValueError):
        return False

    threshold = 1.0 - WEAR_COMPARISON_EPSILON
    return w >= threshold