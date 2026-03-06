"""Refresh the card's value using a provider callback."""

from __future__ import annotations

from core.errors import log_exception


def _refresh_value(self, context: dict = None) -> None:
    """Evaluate and display the latest value from value_provider.

    The provider can accept a single `context` argument, or no arguments.
    This keeps expensive/composed calculations outside the widget.
    """
    if self.value_provider is None:
        return

    context_data = context or {}

    try:
        try:
            value = self.value_provider(context_data)
        except TypeError:
            value = self.value_provider()

        self.value_label.setText(str(value))
    except Exception as exc:
        log_exception(
            exc,
            f'Failed to refresh StatsCard value for "{self.title}"',
            category='stats_strip',
            action='refresh_value',
        )
