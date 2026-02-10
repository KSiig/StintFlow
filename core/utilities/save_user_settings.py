"""
Save user settings to disk.

Persists a settings dictionary to a per-user JSON file.
"""

import json
import os

from core.errors import log, log_exception
from .get_user_settings_path import get_user_settings_path


def save_user_settings(settings: dict) -> None:
    """
    Save settings to the user settings file.

    Args:
        settings: Settings dictionary to persist
    """
    settings_path = get_user_settings_path()
    settings_dir = os.path.dirname(settings_path)

    try:
        os.makedirs(settings_dir, exist_ok=True)
        with open(settings_path, 'w', encoding='utf-8') as file:
            json.dump(settings, file, indent=2)
        log('INFO', 'User settings saved', category='settings', action='save')
    except Exception as e:
        log_exception(e, 'Failed to save user settings', category='settings', action='save')
        raise
