"""Apply strategies stylesheet."""

from core.errors import log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load and apply navigation menu stylesheet."""
    try:
        style_path = resource_path("resources/styles/strategies.qss")
        with open(style_path, "r") as style_file:
            self.setStyleSheet(style_file.read())
    except FileNotFoundError as exc:
        log_exception(exc, "Navigation menu stylesheet not found", category="ui", action="load_stylesheet")
