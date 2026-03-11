"""Persist settings to disk."""

from core.errors import log, log_exception
from core.utilities import load_user_settings, save_user_settings


def _save_settings(self) -> None:
    """Persist settings to disk and update UI state."""
    try:
        current_settings = load_user_settings()
        if not isinstance(current_settings, dict):
            current_settings = {}

        mongo_settings: dict[str, str | None] = {}
        agent_settings: dict[str, str | None] = {}
        strategy_settings: dict[str, int | None] = {}

        agent_field = self.inputs.get("agent_name")
        if agent_field is not None:
            text = agent_field.text().strip()
            agent_settings["name"] = text if text else None

        for key in ("uri", "host", "database", "username", "password", "auth_source"):
            input_field = self.inputs.get(key)
            if input_field is None:
                continue
            value = input_field.text().strip()
            mongo_settings[key] = value if value else None

        logging_settings: dict[str, int | None] = {}
        retention_field = self.inputs.get("retention_days")
        if retention_field is not None:
            text = retention_field.text().strip()
            if text:
                try:
                    retention_val = int(text)
                except ValueError:
                    if self.status_label:
                        self.status_label.setText("Log retention must be a non-negative integer.")
                    return
                if retention_val < 0:
                    if self.status_label:
                        self.status_label.setText("Log retention cannot be negative.")
                    return
                logging_settings["retention_days"] = retention_val
            else:
                logging_settings["retention_days"] = None

        interval_field = self.inputs.get("strategy_auto_sync_interval_seconds")
        if interval_field is not None:
            text = interval_field.text().strip()
            if text:
                # validate numeric and non-negative (validator should prevent bad input,
                # but we guard against unexpected values and provide a user-friendly
                # message rather than a generic failure)
                try:
                    interval_val = int(text)
                except ValueError:
                    if self.status_label:
                        self.status_label.setText("Auto-sync interval must be a non-negative integer.")
                    return
                if interval_val < 0:
                    if self.status_label:
                        self.status_label.setText("Auto-sync interval cannot be negative.")
                    return
                strategy_settings["auto_sync_interval_seconds"] = interval_val
            else:
                strategy_settings["auto_sync_interval_seconds"] = None

        current_settings["agent"] = agent_settings
        current_settings["strategy"] = strategy_settings
        current_settings["mongodb"] = mongo_settings
        current_settings["logging"] = logging_settings
        save_user_settings(current_settings)
        self.reload_button.show()

        if self.status_label:
            self.status_label.setText("Saved. Restart the app to apply changes.")
        log("INFO", "Settings saved from UI", category="settings", action="save_ui")
    except Exception as exc:
        log_exception(exc, "Failed to save settings from UI", category="settings", action="save_ui")
        if self.status_label:
            self.status_label.setText("Failed to save settings.")
