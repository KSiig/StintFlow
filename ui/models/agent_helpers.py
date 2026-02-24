"""
Utilities for converting agent documents into table rows for display.

These helpers are intended to be used by any UI component that wants to
show the list of connected agents.  Documents are expected to come from the
``agents`` collection and contain at least ``name``, ``connected_at`` and
``last_heartbeat`` fields.
"""

from datetime import datetime


def docs_to_rows(docs: list[dict]) -> list[list]:
    """Convert agent documents to table rows.

    Rows have the following columns:
    1. name
    2. connected_at (ISO string)
    3. last_heartbeat (ISO string)

    Args:
        docs: list of agent documents from MongoDB

    Returns:
        list of row lists suitable for a QAbstractTableModel
    """
    rows: list[list] = []
    for doc in docs:
        name = doc.get('name', '')
        connected = doc.get('connected_at')
        heartbeat = doc.get('last_heartbeat')
        rows.append([
            name,
            connected.isoformat() if isinstance(connected, datetime) else connected,
            heartbeat.isoformat() if isinstance(heartbeat, datetime) else heartbeat,
        ])
    return rows
