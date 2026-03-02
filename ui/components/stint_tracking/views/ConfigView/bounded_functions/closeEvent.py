"""Handle cleanup when the ConfigView closes."""


def closeEvent(self, event) -> None:
    """Disconnect signals on close to avoid stray callbacks."""
    try:
        if self.config_options:
            self.config_options.stint_created.disconnect(self.table_model.update_data)
    except Exception:
        pass

    super().closeEvent(event)
