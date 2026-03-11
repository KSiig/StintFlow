"""Row deletion logic for TableModel, including optional DB cleanup."""

from core.database import delete_stint as delete_stint_from_db
from core.errors import log, log_exception


def delete_stint(self, row: int, strategy_id: str = None) -> None:
    """Remove a stint row from DB (if applicable) and model state."""
    if row < 0 or row >= self.rowCount():
        log("WARNING", f"Tried to delete invalid row {row}", category="table_model", action="delete_stint")
        return

    # audit log when a strategy is involved; deletion always attempts below
    if strategy_id:
        log(
            "DEBUG",
            f"Deleting stint at row {row} for strategy {strategy_id}",
            category="table_model",
            action="delete_stint",
        )

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
            extra = f" (strategy={strategy_id})" if strategy_id else ""
            log_exception(
                exc,
                f"Failed to delete stint {stint_id}{extra} from DB: {exc}",
                category="table_model",
                action="delete_stint",
            )

    self.beginResetModel()
    try:
        # perform deletions under reset; guarantee endResetModel() below
        try:
            del self._data[row]
        except Exception as exc:
            # can't safely continue if _data deletion fails; keep lists aligned
            log_exception(
                exc,
                f"Failed to delete row {row} from _data: {exc}",
                category="table_model",
                action="delete_stint",
            )
            return
        try:
            if row < len(self._tires):
                del self._tires[row]
        except Exception as exc:
            log_exception(
                exc,
                f"Failed to delete row {row} from _tires: {exc}",
                category="table_model",
                action="delete_stint",
            )
        try:
            if row < len(self._meta):
                del self._meta[row]
        except Exception as exc:
            log_exception(
                exc,
                f"Failed to delete row {row} from _meta: {exc}",
                category="table_model",
                action="delete_stint",
            )
    finally:
        self.endResetModel()

    try:
        self.update_mean()
    except Exception as exc:
        log_exception(exc, f"Failed to update mean after deleting row {row}: {exc}", category="table_model", action="delete_stint")
