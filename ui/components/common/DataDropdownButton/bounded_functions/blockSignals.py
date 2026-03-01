from PyQt6.QtCore import QObject


def blockSignals(self, blocked: bool) -> bool:
    """Block/unblock signals for this widget."""
    self._signals_blocked = blocked
    return QObject.blockSignals(self, blocked)