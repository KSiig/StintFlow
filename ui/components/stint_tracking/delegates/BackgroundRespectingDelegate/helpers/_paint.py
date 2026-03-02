"""Paint with model-provided background role first."""

from PyQt6.QtCore import Qt


def _paint(self, painter, option, index):
    bg = index.data(Qt.ItemDataRole.BackgroundRole)
    if bg:
        painter.save()
        painter.fillRect(option.rect, bg)
        painter.restore()
    super(type(self), self).paint(painter, option, index)
