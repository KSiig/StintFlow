"""Helper for ConfigOptions that processes tracker output.

This module provides a single function, ``_handle_output``, which bridges
``QProcess`` output streams to the shared
``handle_stint_tracker_output`` parser.  It is responsible for
forwarding the parsed events to the corresponding methods or signals on the
``ConfigOptions`` widget.
"""

from __future__ import annotations

from ui.components.stint_tracking.config import handle_stint_tracker_output


def _handle_output(self, stdout: str) -> None:
    """Parse structured event messages from stint_tracker.

    The ``stdout`` string may contain multiple lines of log output; this
    helper simply forwards it to ``handle_stint_tracker_output`` with the
    widget's callbacks wired up.  No return value is produced.
    """
    handle_stint_tracker_output(
        stdout,
        on_stint_created=lambda: self.stint_created.emit(),
        on_return_to_garage=lambda: self._show_info_lbl("Please return to garage!"),
        on_player_in_garage=self._reset_info_lbl,
        on_no_active_vehicles=self._handle_no_active_vehicles,
        on_registration_conflict=self._handle_agent_registration_conflict,
    )
