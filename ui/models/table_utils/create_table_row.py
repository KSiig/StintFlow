from ui.models.table_constants import ColumnIndex, TableRow


def create_table_row(
    stint_type: str,
    driver: str,
    status: str,
    pit_time: str,
    tires_changed: int,
    tires_left: int,
    stint_time: str,
    time_of_day: str,
) -> TableRow:
    """Create a standardized table row."""
    return [
        stint_type,
        driver,
        status,
        pit_time,
        str(tires_changed),
        str(tires_left),
        stint_time,
        time_of_day,
        "",
    ]
