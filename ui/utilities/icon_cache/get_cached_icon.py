"""Convenience wrapper to fetch icons from the global cache."""

from PyQt6.QtGui import QPixmap

from ui.utilities.icon_cache.IconCache import IconCache


def get_cached_icon(icon_path: str, size: int, color: str = "#FFFFFF") -> QPixmap:
    """Return a cached (or freshly loaded) icon pixmap."""
    cache = IconCache()
    return cache.get_icon(icon_path, size, color)
