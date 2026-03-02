"""Set the popup icon and color."""

from ui.utilities.load_icon import load_icon


def _set_icon(self, popup_type: str) -> None:
    """Set the icon pixmap and color based on the popup type."""
    icon_path, color = self._icon_map.get(popup_type, ("resources/icons/popup/info.svg", "#3b82f6"))
    icon_pixmap = load_icon(icon_path, size=32, color=color)
    self.icon_label.setPixmap(icon_pixmap)
