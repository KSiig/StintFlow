"""
Load user settings from disk.

Returns an empty dictionary if the settings file does not exist or is invalid.
"""

import json

from core.errors import log_exception
from .get_user_settings_path import get_user_settings_path


def load_user_settings() -> dict:
    """
    Load settings from the user settings file.

    Returns:
        Settings dictionary, or empty dict if unavailable.
    """
    settings_path = get_user_settings_path()

    try:
        with open(settings_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception as e:
        log_exception(e, 'Failed to load user settings', category='settings', action='load')
        return {}
