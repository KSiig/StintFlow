"""Persist excluded flag to the database when enabled."""

from core.database import update_stint
from core.errors import log


def _persist_excluded_flag(self, meta: dict) -> None:
    try:
        stint_id = meta.get("id")
        if stint_id:
            update_stint(str(stint_id), {"excluded": bool(meta.get("excluded"))})
    except Exception as exc:
        log("ERROR", f"Failed to persist excluded flag for stint {meta.get('id')}: {exc}", category="actions_delegate", action="persist_excluded")
