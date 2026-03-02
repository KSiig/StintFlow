"""Paint the model-provided BackgroundRole brush if present."""

from PyQt6.QtCore import Qt


def paint_model_background(painter, option, index) -> None:
    bg = index.data(Qt.ItemDataRole.BackgroundRole)
    if bg:
        painter.save()
        painter.fillRect(option.rect, bg)
        painter.restore()
