from ui.components.settings import SettingsView


def show_settings(self) -> None:
    """Switch the main window to the settings view."""
    settings_widget = self.navigation_model.widgets.get(SettingsView)
    if settings_widget:
        self.navigation_model.set_active_widget(settings_widget)
