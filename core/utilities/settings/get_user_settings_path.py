"""
Resolve the user settings file path.

Uses the per-user application data directory and stores settings in a
StintFlow-specific folder.
"""

import os


def get_user_settings_path() -> str:
    """
    Return the absolute path to the user settings file.

    Falls back to the user's home directory if no app data path is available.
    """
    base_dir = os.getenv('APPDATA') or os.getenv('LOCALAPPDATA')
    if not base_dir:
        base_dir = os.path.expanduser('~')

    return os.path.join(base_dir, 'StintFlow', 'settings.json')
