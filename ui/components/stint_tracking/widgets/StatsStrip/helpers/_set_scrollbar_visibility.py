"""Toggle StatsStrip scrollbar visibility based on hover state."""

from PyQt6.QtCore import Qt


def _set_scrollbar_visibility(self, is_visible: bool) -> None:
    """Show or hide the horizontal scrollbar, with a fade animation.

    The actual policy is switched immediately when showing (so layout
    updates) and after the fade completes when hiding (to avoid layout
    jumps while animating).
    """
    if self.scroll_area is None:
        return

    # delegate the animation logic to the fade helper; it will manage
    # policies/hiding internally
    self._fade_scrollbar(is_visible)
