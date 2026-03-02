"""Return the configured MongoDB database handle."""

import os

from core.errors import log
from core.utilities import load_user_settings
from .. import _state
from ..constants import DEFAULT_DATABASE_NAME
from ._get_client import _get_client


def _get_database():
    """Get the application database, creating it if necessary."""
    settings = load_user_settings()
    mongo_settings = settings.get("mongodb", {}) if isinstance(settings, dict) else {}

    database_name = mongo_settings.get("database")
    if isinstance(database_name, str):
        database_name = database_name.strip()
    database_name = database_name or os.getenv("MONGODB_DATABASE", DEFAULT_DATABASE_NAME)

    if _state.db is None or _state.db_name != database_name:
        client = _get_client()
        _state.db = client[database_name]
        _state.db_name = database_name
        log("INFO", f"Using database: {database_name}", category="database", action="get_database")

    return _state.db
