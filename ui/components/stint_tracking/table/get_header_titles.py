"""
Extract header titles from TABLE_HEADERS constant.

Used by code that needs just the string titles for calculations.
"""

from ..constants import TABLE_HEADERS


def get_header_titles():
    """
    Extract just the header titles from TABLE_HEADERS.
    
    Returns:
        list[str]: List of header title strings
    """
    return [header["title"] for header in TABLE_HEADERS]
