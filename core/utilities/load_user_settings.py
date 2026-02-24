"""
Load user settings from disk.

Returns an empty dictionary if the settings file does not exist or is invalid.
"""

import json

# ``log_exception`` is imported lazily inside the function to avoid an
# import cycle: several modules in ``core.errors`` (notably
# ``log_error``/``log_rotation``) import ``load_user_settings``.  If
# this module tried to import ``log_exception`` at top level the
# circular dependency would cause partially-initialised modules to be
# exposed, leading to subtle errors (see GitHub issue).  Local import
# keeps the dependency confined to the error-handling path.
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
        # import log_exception here to avoid circular import problems
        # as noted in the module docstring above.
        from core.errors import log_exception

        log_exception(e, 'Failed to load user settings', category='settings', action='load')
        return {}
