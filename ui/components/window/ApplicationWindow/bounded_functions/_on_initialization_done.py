from ui.components.settings import SettingsView
from ui.components.stint_tracking import ConfigView, OverviewView, StrategiesView
from ui.models import ModelContainer


def _on_initialization_done(self, data, tires, mean_stint_time, events, sessions) -> None:
    """Finalize UI setup once background initialization finishes."""
    self.table_model.update_data(data=data, tires=tires, mean_stint_time=mean_stint_time)

    try:
        if hasattr(self, "navigation_menu") and hasattr(self.navigation_menu, "session_picker"):
            session_picker = self.navigation_menu.session_picker
            session_picker.events.blockSignals(True)
            session_picker.sessions.blockSignals(True)
            session_picker.events.clear()
            for doc in events:
                session_picker.events.addItem(doc.get("name", ""), userData=str(doc.get("_id", "")))
            if events and sessions:
                session_picker.sessions.clear()
                for doc in sessions:
                    session_picker.sessions.addItem(doc.get("name", ""), userData=str(doc.get("_id", "")))
            session_picker.events.blockSignals(False)
            session_picker.sessions.blockSignals(False)
            session_picker.reload(
                selected_event_id=self.selection_model.event_id,
                selected_session_id=self.selection_model.session_id,
            )
    except Exception:
        pass

    models = ModelContainer(selection_model=self.selection_model, table_model=self.table_model)

    overview_view = OverviewView(models)
    self.navigation_model.add_widget(OverviewView, overview_view)

    config_view = ConfigView(models)
    self.navigation_model.add_widget(ConfigView, config_view)

    strategies_view = StrategiesView(models)
    self.navigation_model.add_widget(StrategiesView, strategies_view)

    settings_view = SettingsView(models)
    self.navigation_model.add_widget(SettingsView, settings_view)

    self.navigation_model.set_active_widget(overview_view)

    if hasattr(self, "loading_overlay") and self.loading_overlay:
        self.loading_overlay.hide()
