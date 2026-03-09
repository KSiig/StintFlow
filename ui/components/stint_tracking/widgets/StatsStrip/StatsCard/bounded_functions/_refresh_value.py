"""Refresh the card's value using a provider callback."""

from __future__ import annotations

from core.errors import log_exception


def _refresh_value(self, context: dict | None = None) -> None:
    """Evaluate and display the latest value from value_provider.

    The provider can accept a single `context` argument, or no arguments.
    This keeps expensive/composed calculations outside the widget.
    """
    if self.value_provider is None:
        return

    context_data = context or {}

    try:
        try:
            value_result = self.value_provider(context_data)
        except TypeError:
            value_result = self.value_provider()

        value = value_result
        value_right = None
        if isinstance(value_result, (tuple, list)) and len(value_result) >= 2:
            value = value_result[0]
            value_right = value_result[1]

        self.value_label.setText(str(value))

        if self.value_right_label is not None:
            self.value_right_text = "" if value_right is None else str(value_right)
            self.value_right_label.setText(self.value_right_text)
            self.value_right_label.setVisible(bool(self.value_right_text))
    except Exception as exc:
        log_exception(
            exc,
            f'Failed to refresh StatsCard value for "{self.title}"',
            category='stats_strip',
            action='refresh_value',
        )
