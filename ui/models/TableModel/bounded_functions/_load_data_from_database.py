"""Load table data from the database and initialize model state."""

from core.errors import log
from ui.models.table_loader._build_table_data_payload import _build_table_data_payload

from ..constants import DEFAULT_TIRE_COUNT


def _load_data_from_database(self) -> None:
    """Load stint data from database and convert to table format."""
    if not self.selection_model.event_id or not self.selection_model.session_id:
        log("WARNING", "No event or session selected - cannot load data", category="table_model", action="load_data")
        return

    log(
        "DEBUG",
        f"Loading data for event {self.selection_model.event_id}, session {self.selection_model.session_id}",
        category="table_model",
        action="load_data",
    )

    payload = _build_table_data_payload(self.selection_model, self._parse_pit_time)
    if payload is None:
        return

    total_tires = payload["total_tires"]

    try:
        self._event_tire_count = int(total_tires)
    except (ValueError, TypeError):
        self._event_tire_count = int(DEFAULT_TIRE_COUNT)

    stints = payload["stints"]

    self._tires = payload["tires"]
    self._meta = [
        {"id": str(stint.get("_id")), "excluded": bool(stint.get("excluded", False))}
        for stint in stints
    ]

    self._data = payload["rows"]
    self._mean_stint_time = payload["mean_stint_time"]

    self._recalculate_stint_types()
    self._repaint_table()
