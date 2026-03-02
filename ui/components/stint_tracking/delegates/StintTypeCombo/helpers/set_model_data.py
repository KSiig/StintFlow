"""Persist stint type selection to model (and DB when enabled)."""

from PyQt6.QtCore import Qt

from core.database import update_strategy, update_stint
from core.errors import log
from ui.models.TableRoles import TableRoles
from ui.models.stint_helpers import sanitize_stints


def set_model_data(self, editor, model, index):
    old_value = model.data(index, Qt.ItemDataRole.DisplayRole)
    new_value = editor.dropdown.get_value()

    if new_value == old_value:
        return

    model.setData(index, new_value)
    model._recalculate_tires_changed(index, old_value)

    row_data, tire_data, _ = model.get_all_data()
    sanitized_data = sanitize_stints(row_data, tire_data)

    if self.update_doc and self.strategy_id:
        update_strategy(self.strategy_id, sanitized_data)
    elif self.update_doc:
        rows_to_update = min(len(sanitized_data.get("tires", [])), model.rowCount())
        updated_count = 0
        for row_index in range(rows_to_update):
            meta = model.data(model.index(row_index, 0), TableRoles.MetaRole)
            if not meta or "id" not in meta:
                continue
            stint_id = meta["id"]
            row = sanitized_data["tires"][row_index]
            if update_stint(stint_id, {"tire_data": row}):
                updated_count += 1
        if updated_count == 0:
            log("WARNING", "No stints updated from stint type change", category="stint_type_combo", action="set_model_data")
    else:
        log("DEBUG", "Database update skipped (update_doc=False or no strategy_id)", category="stint_type_combo", action="set_model_data")
