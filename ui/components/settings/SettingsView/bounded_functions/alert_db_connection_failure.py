"""Show an error dialog when the database connection fails."""

from ui.components.common import PopUp


def alert_db_connection_failure(self) -> None:
    """Display a message indicating the database connection failed."""
    dialog = PopUp(
        title="Database Connection Failed",
        message="Unable to connect to MongoDB. Please check your settings.",
        buttons=["Ok"],
        type="critical",
        parent=self,
    )
    dialog.exec()
