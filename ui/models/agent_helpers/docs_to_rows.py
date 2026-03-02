"""Convert agent documents into table rows for display."""

from datetime import datetime


def docs_to_rows(docs: list[dict]) -> list[list]:
    """Convert agent documents to table rows."""
    rows: list[list] = []
    for doc in docs:
        name = doc.get("name", "")
        connected = doc.get("connected_at")
        heartbeat = doc.get("last_heartbeat")
        rows.append(
            [
                name,
                connected.isoformat() if isinstance(connected, datetime) else connected,
                heartbeat.isoformat() if isinstance(heartbeat, datetime) else heartbeat,
            ]
        )
    return rows
