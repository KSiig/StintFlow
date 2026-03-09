from __future__ import annotations


def _handle_no_active_vehicles(self) -> None:
    """Show a no-active-session warning and stop tracking."""
    self._toggle_track()
    self._open_popup(
        title="No active session found",
        message=(
            "No active session was found. Make sure you are in an active session, "
            "then try starting the tracker again."
        ),
        buttons=["Ok"],
        type="error",
    )