"""Paint background before default rendering."""

from ui.components.stint_tracking.delegates.delegate_utils import paint_model_background


def paint(self, painter, option, index):
    paint_model_background(painter, option, index)
    super(type(self), self).paint(painter, option, index)
