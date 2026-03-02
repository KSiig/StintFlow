"""Singleton cache for loaded and colorized icons."""

from PyQt6.QtGui import QPixmap

from ui.utilities.load_icon import load_icon


class IconCache:
    """Cache icons by (path, size, color) to avoid redundant I/O."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
        return cls._instance

    def get_icon(self, icon_path: str, size: int, color: str = "#FFFFFF") -> QPixmap:
        """Load an icon with caching; returns a QPixmap (possibly null)."""
        cache_key = (icon_path, size, color)
        if cache_key in self._cache:
            return self._cache[cache_key]

        pixmap = load_icon(icon_path, size, color)
        self._cache[cache_key] = pixmap
        return pixmap

    def clear(self) -> None:
        """Clear the icon cache."""
        self._cache.clear()

    def get_cache_size(self) -> int:
        """Return the number of cached icons."""
        return len(self._cache)
