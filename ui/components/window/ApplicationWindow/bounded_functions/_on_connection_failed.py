from ui.components.settings import SettingsView
from ui.models import ModelContainer


def _on_connection_failed(self) -> None:
    """Switch to settings pane when DB connection fails."""
    if hasattr(self, "loading_overlay") and self.loading_overlay:
        self.loading_overlay.set_status("Connection failed")

    models = ModelContainer(selection_model=self.selection_model)
    settings_view = SettingsView(models)
    self.navigation_model.add_widget(SettingsView, settings_view)
    self.navigation_model.set_active_widget(settings_view)
    settings_view.alert_db_connection_failure()

    if hasattr(self, "loading_overlay") and self.loading_overlay:
        self.loading_overlay.hide()
