"""Load settings from disk into the UI."""

from core.errors import log_exception
from core.utilities import load_user_settings


def _load_settings(self) -> None:
    """Load settings from disk and populate inputs."""
    try:
        settings = load_user_settings()
        mongo_settings = settings.get("mongodb", {}) if isinstance(settings, dict) else {}
        logging_settings = settings.get("logging", {}) if isinstance(settings, dict) else {}
        agent_settings = settings.get("agent", {}) if isinstance(settings, dict) else {}
        strategy_settings = settings.get("strategy", {}) if isinstance(settings, dict) else {}
        mongo_defaults = self._get_default_mongo_settings()
        log_defaults = self._get_default_logging_settings()
        agent_defaults = self._get_default_agent_settings()
        strategy_defaults = self._get_default_strategy_settings()
        agent_field = self.inputs.get("agent_name")
        if agent_field is not None:
            value = agent_settings.get("name")
            if isinstance(value, str):
                value = value.strip()
            if not value:
                value = agent_defaults.get("name", "")
            agent_field.setText(value or "")

        for key in ("uri", "host", "database", "username", "password", "auth_source"):
            input_field = self.inputs.get(key)
            if not input_field:
                continue
            value = mongo_settings.get(key)
            if isinstance(value, str):
                value = value.strip()
            if not value:
                value = mongo_defaults.get(key, "")
            input_field.setText(value or "")

        retention_field = self.inputs.get("retention_days")
        if retention_field is not None:
            value = logging_settings.get("retention_days")
            if value is None:
                value = log_defaults.get("retention_days", "")
            retention_field.setText(str(value) if value is not None else "")

        # strategy-specific inputs
        interval_field = self.inputs.get("strategy_auto_sync_interval_seconds")
        if interval_field is not None:
            value = strategy_settings.get("auto_sync_interval_seconds")
            if value is None:
                value = strategy_defaults.get("auto_sync_interval_seconds", "")
            interval_field.setText(str(value) if value is not None else "")

        if self.status_label:
            self.status_label.setText("")
    except Exception as exc:
        log_exception(exc, "Failed to load settings into UI", category="settings", action="load_ui")
        if self.status_label:
            self.status_label.setText("Failed to load settings.")
