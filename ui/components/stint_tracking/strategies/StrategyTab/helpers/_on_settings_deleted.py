from __future__ import annotations


def _on_settings_deleted(self, strategy_id: str) -> None:
    """Propagate strategy deletion up to container view."""
    self.deleted.emit(strategy_id)
