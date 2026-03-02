"""Toggle excluded flag and refresh model/state."""

from ui.models.TableRoles import TableRoles


def _toggle_exclude(self, row: int, model, option) -> None:
    meta = model.data(model.index(row, 0), TableRoles.MetaRole) or {}
    if not isinstance(meta, dict):
        meta = {}
    meta["excluded"] = not bool(meta.get("excluded"))
    model.setData(model.index(row, 0), meta, role=TableRoles.MetaRole)

    if option.widget is not None:
        option.widget.viewport().update()

    try:
        if hasattr(model, "update_mean"):
            is_strat = getattr(model, "_is_strategy", False)
            model.update_mean(update_pending=not is_strat)
    except Exception:
        pass

    if self.update_doc:
        self._persist_excluded_flag(meta)
