"""Persist tire popup selections to model and DB if enabled."""

import copy

from core.database import update_strategy, update_stint
from core.errors import log
from ui.models.TableRoles import TableRoles
from ui.models.stint_helpers import sanitize_stints


def set_model_data(self, editor, model, index):
    values = editor.popup.values()
    values_lowered = {k.lower(): v.lower() for k, v in values.items()}

    old_value = model.data(index, TableRoles.TiresRole)
    new_value = copy.deepcopy(old_value)

    for tire, compound in values_lowered.items():
        new_value["tires_changed"][tire] = bool(compound)
        if compound:
            new_value[tire]["outgoing"]["compound"] = compound

    if new_value == old_value:
        return

    model.setData(index, new_value, TableRoles.TiresRole)
    model._recalculate_tires_left()

    row_data, tire_data, _ = model.get_all_data()
    sanitized_data = sanitize_stints(row_data, tire_data)

    if self.update_doc and self.strategy_id:
        update_strategy(self.strategy_id, sanitized_data)
    elif self.update_doc:
        stint_id = model.data(index, TableRoles.MetaRole)["id"]
        row = sanitized_data["tires"][index.row()]
        update_stint(stint_id, {"tire_data": row})
    else:
        log("INFO", "Database update skipped (update_doc=False or no strategy_id)", category="tire_combo_delegate", action="set_model_data")
