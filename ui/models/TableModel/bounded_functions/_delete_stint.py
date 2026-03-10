"""Row deletion logic for TableModel, including optional DB cleanup."""

from core.database import delete_stint as delete_stint_from_db
from core.errors import log


def delete_stint(self, row: int, strategy_id: str = None) -> None:
    """Remove a stint row from DB (if applicable) and model state."""
    if row < 0 or row >= self.rowCount():
        log("WARNING", f"Tried to delete invalid row {row}", category="table_model", action="delete_stint")
        return

    if strategy_id:
        log(
            "DEBUG",
            f"Deleting stint at row {row} for strategy {strategy_id}",
            category="table_model",
            action="delete_stint",
        )
    else:
        stint_id = None
        try:
            meta = self._meta[row] if row < len(self._meta) else None
            stint_id = meta.get("id") if isinstance(meta, dict) else None
        except Exception:
            stint_id = None

        if stint_id:
            try:
                delete_stint_from_db(str(stint_id))
            except Exception as exc:  # pragma: no cover - defensive logging
                log(
                    "ERROR",
                    f"Failed to delete stint {stint_id} from DB: {exc}",
                    category="table_model",
                    action="delete_stint",
                )

    self.beginResetModel()
    try:
        del self._data[row]
    except Exception:
        pass
    try:
        if row < len(self._tires):
            del self._tires[row]
    except Exception:
        pass
    try:
        if row < len(self._meta):
            del self._meta[row]
    except Exception:
        pass
    self.endResetModel()

    try:
        self.update_mean()
    except Exception:
        pass
