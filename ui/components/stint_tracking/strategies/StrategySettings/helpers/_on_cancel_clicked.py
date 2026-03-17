from __future__ import annotations

"""Click handler helpers for the StrategySettings panel.

This module provides the handler invoked when the user clicks the "Cancel" button
in StrategySettings, restoring the last committed values and clearing the
unsaved-change state.
"""


def _on_cancel_clicked(self) -> None:
    """Restore the last committed strategy settings values."""
    if self._committed_input_state is None:
        return

    self._apply_input_state(self._committed_input_state, persist_as_committed=True)
