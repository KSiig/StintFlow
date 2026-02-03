"""
Get header icon filename by column index.

Retrieves the icon path for a specific table header column.
"""

from .constants import TABLE_HEADERS


def get_header_icon(index):
    """
    Get the icon filename for a header by index.
    
    Args:
        index: Column index (0-based)
        
    Returns:
        str: Icon filename, or None if index is out of range
    """
    if 0 <= index < len(TABLE_HEADERS):
        return TABLE_HEADERS[index]["icon"]
    return None
