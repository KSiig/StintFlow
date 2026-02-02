"""
Icon cache utility for efficient icon loading and caching.

Provides a singleton cache for SVG icons to avoid reloading the same icons
multiple times. Icons are cached by (path, size, color) tuple.
"""

from PyQt6.QtGui import QPixmap
from ui.utilities.load_icon import load_icon


class IconCache:
    """
    Singleton cache for loaded and colorized icons.
    
    Caches icons by (path, size, color) to avoid redundant file I/O and
    processing. Cache persists for the lifetime of the application unless
    explicitly cleared.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
        return cls._instance
    
    def get_icon(self, icon_path: str, size: int, color: str = "#FFFFFF") -> QPixmap:
        """
        Load an icon with caching.
        
        Icons are cached by (path, size, color) tuple. Subsequent requests for
        the same icon return the cached pixmap without reloading from disk.
        
        Args:
            icon_path: Path to the SVG icon file
            size: Size to scale the icon to (width and height)
            color: Hex color code to apply to the icon (default: white)
            
        Returns:
            QPixmap of the loaded and colorized icon, or null pixmap if loading fails
        """
        cache_key = (icon_path, size, color)
        
        # Return cached icon if available
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Load icon using utility function
        pixmap = load_icon(icon_path, size, color)
        
        # Cache the result (even if null, to avoid repeated failed loads)
        self._cache[cache_key] = pixmap
        
        return pixmap
    
    def clear(self) -> None:
        """
        Clear the icon cache.
        
        Removes all cached icons to free memory. Icons will be reloaded
        from disk on next access.
        """
        self._cache.clear()
    
    def get_cache_size(self) -> int:
        """
        Get the number of cached icons.
        
        Returns:
            Number of unique (path, size, color) combinations currently cached
        """
        return len(self._cache)


def get_cached_icon(icon_path: str, size: int, color: str = "#FFFFFF") -> QPixmap:
    """
    Convenience function to get an icon from the global cache.
    
    Args:
        icon_path: Path to the SVG icon file
        size: Size to scale the icon to (width and height)
        color: Hex color code to apply to the icon (default: white)
        
    Returns:
        QPixmap of the loaded and colorized icon
    """
    cache = IconCache()
    return cache.get_icon(icon_path, size, color)
