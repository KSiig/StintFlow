"""
Helper function for converting MongoDB strategy documents to table rows.

Converts strategy stint documents from MongoDB format to table row format
with proper data types (timedelta, integers, status strings).
"""

from datetime import timedelta


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
        ...         "stint_time_seconds": 3600
        ...     }
        ... ]
        >>> rows = mongo_docs_to_rows(docs)
        >>> rows[0][6]  # stint time
        timedelta(seconds=3600)
    """
    rows = []

    for doc in docs:
        row = [
            doc.get("stint_type"),
            doc.get("name"),
            "Completed" if doc.get("status") else "Pending",
            doc.get("pit_end_time"),
            int(doc.get("tires_changed", 0)),
            int(doc.get("tires_left", 0)),
            timedelta(seconds=int(doc.get("stint_time_seconds", 0))),
            "" # Placeholder for actions column
        ]
        rows.append(row)

    return rows
