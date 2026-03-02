"""Convert stint type label to numeric length."""


def get_stint_length(stint_type: str) -> int:
    """Return stint length (defaults to 1 when unknown)."""
    if not stint_type:
        return 1

    mapping = {
        "Single": 1,
        "Double": 2,
        "Triple": 3,
        "Quadruple": 4,
        "Quintuple": 5,
        "Sextuple": 6,
        "Septuple": 7,
        "Octuple": 8,
        "Nonuple": 9,
        "Decuple": 10,
    }
    return mapping.get(stint_type, 1)
