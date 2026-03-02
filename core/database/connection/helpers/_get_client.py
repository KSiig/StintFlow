"""Create or return the shared MongoDB client."""

import os
import warnings
from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from core.errors import log, log_exception
from core.utilities import load_user_settings
from .. import _state
from ..constants import (
    CONNECTION_TIMEOUT_MS,
    DEFAULT_MONGODB_HOST,
    MAX_POOL_SIZE,
    SERVER_SELECTION_TIMEOUT_MS,
)
from ._validate_host import _validate_host

# Suppress CosmosDB compatibility warnings from PyMongo
warnings.filterwarnings(
    "ignore",
    message="You appear to be connected to a CosmosDB cluster.*",
    category=UserWarning,
)


def _get_client() -> MongoClient:
    """Get or create the MongoDB client connection."""
    settings = load_user_settings()
    mongo_settings = settings.get("mongodb", {}) if isinstance(settings, dict) else {}

    uri = mongo_settings.get("uri")
    host = mongo_settings.get("host")
    username = mongo_settings.get("username")
    password = mongo_settings.get("password")
    auth_source = mongo_settings.get("auth_source")

    if isinstance(uri, str):
        uri = uri.strip()
    if isinstance(host, str):
        host = host.strip()
    if isinstance(username, str):
        username = username.strip()
    if isinstance(password, str):
        password = password.strip()
    if isinstance(auth_source, str):
        auth_source = auth_source.strip()

    uri = uri or os.getenv("MONGODB_URI")
    host = host or os.getenv("MONGODB_HOST", DEFAULT_MONGODB_HOST)
    username = username or os.getenv("MONGODB_USERNAME")
    password = password or os.getenv("MONGODB_PASSWORD")
    auth_source = auth_source or os.getenv("MONGODB_AUTH_SOURCE")

    if not uri and not _validate_host(host):
        error_msg = f"Invalid MongoDB host format: {host} (expected hostname or hostname:port)"
        log("ERROR", error_msg, category="database", action="validate_host")
        raise ValueError(error_msg)

    current_config: dict[str, Any] = {
        "uri": uri,
        "host": host,
        "username": username,
        "password": password,
        "auth_source": auth_source,
    }

    if _state.client is None or _state.client_config != current_config:
        if _state.client is not None and _state.client_config != current_config:
            try:
                _state.client.close()
            except Exception as exc:
                log_exception(
                    exc,
                    "Failed to close existing MongoDB connection",
                    category="database",
                    action="disconnect",
                )
            _state.client = None
            _state.db = None
            _state.db_name = None

        _state.client_config = current_config

        try:
            if uri:
                log(
                    "INFO",
                    "Connecting to MongoDB using connection string",
                    category="database",
                    action="connect",
                )
            else:
                log(
                    "INFO",
                    f"Connecting to MongoDB at {host}",
                    category="database",
                    action="connect",
                )

            if uri:
                _state.client = MongoClient(
                    uri,
                    connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                    serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                    maxPoolSize=MAX_POOL_SIZE,
                )
            else:
                auth_kwargs: dict[str, Any] = {}
                if username and password:
                    auth_kwargs = {"username": username, "password": password}
                    if auth_source:
                        auth_kwargs["authSource"] = auth_source
                elif username or password:
                    log(
                        "WARNING",
                        "MongoDB username/password incomplete; ignoring credentials",
                        category="database",
                        action="connect",
                    )

                _state.client = MongoClient(
                    host,
                    connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                    serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                    maxPoolSize=MAX_POOL_SIZE,
                    **auth_kwargs,
                )

            _state.client.server_info()
            log("INFO", "MongoDB connection established", category="database", action="connect")

        except (ConnectionFailure, ServerSelectionTimeoutError) as exc:
            log_exception(exc, "Failed to connect to MongoDB", category="database", action="connect")
            _state.client = None
            raise
        except Exception as exc:
            log_exception(exc, "Unexpected error connecting to MongoDB", category="database", action="connect")
            _state.client = None
            raise
    else:
        try:
            _state.client.server_info()
        except (ConnectionFailure, ServerSelectionTimeoutError):
            log("WARNING", "MongoDB connection lost, reconnecting...", category="database", action="reconnect")
            _state.client = None
            return _get_client()

    return _state.client
