"""
Helper function for converting MongoDB strategy documents to table rows.

Converts strategy stint documents from MongoDB format to table row format
with properly formatted string values (zero-padded HH:MM:SS) for time
fields, plus integers and status strings.
"""

from datetime import timedelta

from ui.models.stint_helpers import format_timedelta


def mongo_docs_to_rows(docs: list[dict]) -> list[list]:
    """
    Convert MongoDB strategy documents to table row format.
    
    Args:
        docs: List of strategy stint documents from MongoDB
        
    Returns:
        List of table rows with properly formatted data
        
    Example:
        >>> docs = [
        ...     {
        ...         "stint_type": "Single",
        ...         "name": "Driver 1",
        ...         "status": True,
        ...         "pit_end_time": "01:30:00",
        ...         "tires_changed": 4,
        ...         "tires_left": 8,
        ...         "stint_time_seconds": 3600,
        ...         "time_of_day_seconds": 0
        ...     }
        ... ]
        >>> rows = mongo_docs_to_rows(docs)
        >>> rows[0][6]  # stint time
        '01:00:00'
        >>> rows[0][7]  # time of day
        '00:00:00'
    """
    rows = []

    for doc in docs:
        # convert stored seconds to formatted strings for display
        stint_td = timedelta(seconds=int(doc.get("stint_time_seconds", 0)))
        tod_td = timedelta(seconds=int(doc.get("time_of_day_seconds", 0)))
        row = [
            doc.get("stint_type"),
            doc.get("name"),
            "Completed" if doc.get("status") else "Pending",
            doc.get("pit_end_time"),
            int(doc.get("tires_changed", 0)),
            int(doc.get("tires_left", 0)),
            format_timedelta(stint_td),
            format_timedelta(tod_td),
            "" # Placeholder for actions column
        ]
        rows.append(row)

    return rows
