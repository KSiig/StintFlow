"""
Resolve resource file paths for the application.

Handles both PyInstaller bundled and development environments by using
sys._MEIPASS when bundled, or the current working directory for development.
"""

import os
import sys


def resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    
    Args:
        relative_path (str): Path relative to the resources root
        
    Returns:
        str: Absolute path to the resource
        
    This function handles both PyInstaller bundled applications (which have
    sys._MEIPASS set) and development environments (where it falls back to
    the current working directory).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
