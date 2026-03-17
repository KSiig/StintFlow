"""Guard navigation menu switches when other views have unsaved edits."""
from PyQt6.QtWidgets import QWidget


def _can_switch_menu_item(self, target_widget: QWidget) -> bool:
    """Return whether the navigation menu may switch to the target widget."""
    if not self.models or not self.models.navigation_model:
        return True

    if target_widget == self.models.navigation_model.active_widget:
        return True

    selection_model = self.models.selection_model if self.models else None
    guard = getattr(selection_model, 'view_change_guard', None) if selection_model else None
    if callable(guard):
        return bool(guard())

    return True