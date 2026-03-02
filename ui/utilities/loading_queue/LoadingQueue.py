"""Stacked loading-message queue for the global loading overlay.

Usage:
    # Once, during window setup:
    LoadingQueue.register_window(app_window)

    # At any call site:
    LoadingQueue.push("Saving strategy...")
    try:
        ...
    finally:
        LoadingQueue.pop("Saving strategy...")

The overlay is shown when the first message is pushed and hidden when the
last message is popped. While multiple messages are queued the displayed text
is always the one at index 0 (earliest push still outstanding).
"""

from __future__ import annotations


class LoadingQueue:
    """Singleton that manages stacked loading messages."""

    _messages: list[str] = []
    _window = None  # reference to ApplicationWindow (or any obj with loading_overlay)

    # ------------------------------------------------------------------ #
    # Registration                                                        #
    # ------------------------------------------------------------------ #

    @classmethod
    def register_window(cls, window) -> None:
        """Bind the queue to a window that owns a loading_overlay."""
        cls._window = window

    # ------------------------------------------------------------------ #
    # Public API                                                          #
    # ------------------------------------------------------------------ #

    @classmethod
    def push(cls, message: str) -> None:
        """Add a message and show the overlay if this is the first entry."""
        was_empty = not cls._messages
        cls._messages.append(message)

        if was_empty:
            # First message - show the overlay with this message
            cls._show(cls._messages[0])
        else:
            # Overlay already shown; update label to earliest message (unchanged)
            cls._update_label()

    @classmethod
    def pop(cls, message: str) -> None:
        """Remove a message; hide overlay when queue empties."""
        if message in cls._messages:
            cls._messages.remove(message)

        if not cls._messages:
            cls._hide()
        else:
            cls._update_label()

    @classmethod
    def clear(cls) -> None:
        """Empty the queue and hide the overlay immediately."""
        cls._messages.clear()
        cls._hide()

    # ------------------------------------------------------------------ #
    # Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @classmethod
    def _show(cls, message: str) -> None:
        """Show the overlay with the given message."""
        if cls._window and hasattr(cls._window, "show_loading"):
            cls._window.show_loading(message)

    @classmethod
    def _hide(cls) -> None:
        """Hide the overlay."""
        if cls._window and hasattr(cls._window, "hide_loading"):
            cls._window.hide_loading()

    @classmethod
    def _update_label(cls) -> None:
        """Update the overlay text to the current front message."""
        if not cls._messages:
            return
        if (
            cls._window
            and hasattr(cls._window, "loading_overlay")
            and cls._window.loading_overlay
        ):
            cls._window.loading_overlay.set_status(cls._messages[0])
