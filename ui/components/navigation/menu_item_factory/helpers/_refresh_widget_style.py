"""Force Qt to reapply stylesheet to a widget tree."""

from PyQt6.QtWidgets import QWidget


def _refresh_widget_style(widget: QWidget) -> None:
    """Unpolish/polish children then the widget itself."""
    for child in widget.findChildren(QWidget):
        child.style().unpolish(child)
        child.style().polish(child)

    widget.style().unpolish(widget)
    widget.style().polish(widget)
