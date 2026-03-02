"""Count tire changes in stint tire data."""

from ..table_constants import TireData


def count_tire_changes(tire_data: TireData) -> tuple[int, int]:
    """Return counts of total and medium-compound tire changes."""
    total_changed = 0
    medium_changed = 0

    for tire in ["fl", "fr", "rl", "rr"]:
        is_changed = tire_data.get("tires_changed", {}).get(tire, False)
        compound = tire_data.get(tire, {}).get("outgoing", {}).get("compound", "").lower()

        if is_changed:
            total_changed += 1
            if compound == "medium":
                medium_changed += 1

    return total_changed, medium_changed
