"""Normalize dropdown item inputs into a uniform structure."""

from PyQt6.QtGui import QIcon


def _normalize_items(self, items: list) -> list[dict]:
    """Convert raw item descriptions into normalized dicts."""
    normalized: list[dict] = []
    for it in items:
        display = ''
        value = None
        icon = None
        if isinstance(it, dict):
            display = it.get('display') or it.get('text', '')
            value = it.get('value', display)
            icon = it.get('icon')
        elif isinstance(it, tuple):
            if len(it) == 1:
                display = str(it[0])
                value = display
            elif len(it) == 2:
                second = it[1]
                if isinstance(second, (str, QIcon)) and (
                    isinstance(second, str) and (second.endswith('.png') or second.endswith('.svg'))
                ):
                    display = str(it[0])
                    value = display
                    icon = second
                else:
                    display = str(it[0])
                    value = second
            else:
                display = str(it[0])
                value = it[1]
                icon = it[2]
        else:
            display = str(it)
            value = display
        if isinstance(icon, str):
            icon = QIcon(icon)
        if value is None:
            value = display
        normalized.append({'display': display, 'value': value, 'icon': icon})
    return normalized
