"""Load strategies for the current session and populate tabs."""

from core.errors import log, log_exception
from core.database import get_strategies


def _load_strategies(self) -> None:
    """Load strategies for current session and populate tabs."""
    try:
        session_id = self.selection_model.session_id
        if not session_id:
            log("DEBUG", "No session selected - clearing strategy tabs", category="strategies_view", action="load_strategies")
            self._clear_tabs()
            return

        strategies = list(get_strategies(session_id))

        if not strategies:
            log("INFO", "No strategies found - creating default strategy", category="strategies_view", action="load_strategies")
            default_strategy = self._on_create_strategy(name="Default")
            strategies = [default_strategy] if default_strategy else []

        self._clear_tabs()

        for strategy in strategies:
            tab = self._create_strategy_tab(strategy)
            self._add_tab(tab, strategy["name"])
    except Exception as exc:
        log_exception(exc, "Failed to load strategies", category="strategies_view", action="load_strategies")
