"""Helpers to detect tire changes after a pit stop.

The public `detect_tire_changes` function inspects outgoing tire data and
returns a simple mapping of position codes to booleans indicating whether
the tyre was replaced. The implementation uses a small epsilon defined in
the constants module to avoid brittle float comparisons.
"""

from typing import Any, Dict, Mapping

from .constants import TIRE_POSITIONS
from ._is_new_tire import _is_new_tire


TyreData = Mapping[str, Any]


def _detect_tire_changes(tires_outgoing: Mapping[str, TyreData]) -> Dict[str, bool]:
    """Return which tyres were replaced during a pit stop.

    The function accepts a mapping keyed by tyre position codes ("fl","fr",
    "rl","rr") where each value is a mapping that may include a numeric
    `wear` key (0.0..1.0). Non-mapping values or absent `wear` keys are
    treated as non-new tyres.
    """
    result: Dict[str, bool] = {}

    for pos in TIRE_POSITIONS:
        outgoing = tires_outgoing.get(pos, {})
        wear = outgoing.get("wear") if isinstance(outgoing, Mapping) else None
        result[pos] = _is_new_tire(wear)

    return result
