"""Convert stint count to a human-readable type name."""


def get_stint_type(stint_amount: int) -> str:
    """Return a type label such as "Single", "Double", etc."""
    mapping = {
        0: "Single",
        1: "Double",
        2: "Triple",
        3: "Quadruple",
        4: "Quintuple",
        5: "Sextuple",
        6: "Septuple",
        7: "Octuple",
        8: "Nonuple",
        9: "Decuple",
    }
    return mapping.get(stint_amount, "Unknown")
