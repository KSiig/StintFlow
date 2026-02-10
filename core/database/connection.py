"""
MongoDB database connection and collection definitions.

Establishes a single MongoDB client connection and defines all database collections
used throughout the application. Uses environment variables for configuration with
sensible defaults for development.

Usage:
    from core.database.connection import stints_col, events_col, sessions_col
    
    # Use collections directly
    events = events_col.find()
"""

import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from core.errors import log, log_exception
from core.utilities import load_user_settings


# MongoDB connection configuration
DEFAULT_MONGODB_HOST = 'localhost:27017'
DEFAULT_DATABASE_NAME = 'stintflow'
CONNECTION_TIMEOUT_MS = 5000  # 5 seconds
SERVER_SELECTION_TIMEOUT_MS = 5000  # 5 seconds
MAX_POOL_SIZE = 10  # Suitable for desktop application

# Global MongoDB client (initialized once)
_client: MongoClient | None = None
_db: Database | None = None
_db_name: str | None = None
_client_config: dict | None = None


def _validate_host(host: str) -> bool:
    """
    Validate MongoDB host string format.
    
    Args:
        host: MongoDB host string (e.g., 'localhost:27017')
        
    Returns:
        True if valid, False otherwise
    """
    if not host:
        return False

    if ':' not in host:
        return True

    parts = host.split(':')
    if len(parts) != 2:
        return False

    try:
        port = int(parts[1])
        return 1 <= port <= 65535
    except ValueError:
        return False


def _get_client() -> MongoClient:
    """
    Get or create the MongoDB client connection.
    
    Creates a single client instance that's reused across the application.
    Connection is established lazily on first use. Includes automatic reconnection
    handling if the connection is lost.
    
    Returns:
        MongoClient instance
        
    Raises:
        ConnectionFailure: If connection cannot be established
        ValueError: If MONGODB_HOST format is invalid
    """
    global _client, _client_config, _db, _db_name
    
    settings = load_user_settings()
    mongo_settings = settings.get('mongodb', {}) if isinstance(settings, dict) else {}

    uri = mongo_settings.get('uri')
    host = mongo_settings.get('host')
    username = mongo_settings.get('username')
    password = mongo_settings.get('password')
    auth_source = mongo_settings.get('auth_source')

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

    uri = uri or os.getenv('MONGODB_URI')
    host = host or os.getenv('MONGODB_HOST', DEFAULT_MONGODB_HOST)
    username = username or os.getenv('MONGODB_USERNAME')
    password = password or os.getenv('MONGODB_PASSWORD')
    auth_source = auth_source or os.getenv('MONGODB_AUTH_SOURCE')

    # Validate host format when using host-based connection
    if not uri and not _validate_host(host):
        error_msg = f'Invalid MongoDB host format: {host} (expected hostname or hostname:port)'
        log('ERROR', error_msg, category='database', action='validate_host')
        raise ValueError(error_msg)

    current_config = {
        'uri': uri,
        'host': host,
        'username': username,
        'password': password,
        'auth_source': auth_source
    }
    
    # Create new client if none exists or test existing connection
    if _client is None or _client_config != current_config:
        if _client is not None and _client_config != current_config:
            try:
                _client.close()
            except Exception as e:
                log_exception(e, 'Failed to close existing MongoDB connection',
                             category='database', action='disconnect')
            _client = None
            _db = None
            _db_name = None

        _client_config = current_config

        try:
            if uri:
                log('INFO', 'Connecting to MongoDB using connection string',
                    category='database', action='connect')
            else:
                log('INFO', f'Connecting to MongoDB at {host}', 
                    category='database', action='connect')

            if uri:
                _client = MongoClient(
                    uri,
                    connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                    serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                    maxPoolSize=MAX_POOL_SIZE
                )
            else:
                auth_kwargs = {}
                if username and password:
                    auth_kwargs = {
                        'username': username,
                        'password': password
                    }
                    if auth_source:
                        auth_kwargs['authSource'] = auth_source
                elif username or password:
                    log('WARNING', 'MongoDB username/password incomplete; ignoring credentials',
                        category='database', action='connect')
                
                _client = MongoClient(
                    host,
                    connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                    serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                    maxPoolSize=MAX_POOL_SIZE,
                    **auth_kwargs
                )
            
            # Test the connection
            _client.server_info()
            log('INFO', 'MongoDB connection established', 
                category='database', action='connect')
                
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            log_exception(e, 'Failed to connect to MongoDB', 
                         category='database', action='connect')
            _client = None
            raise
        except Exception as e:
            log_exception(e, f'Unexpected error connecting to MongoDB', 
                         category='database', action='connect')
            _client = None
            raise
    else:
        # Test existing connection and reconnect if needed
        try:
            _client.server_info()
        except (ConnectionFailure, ServerSelectionTimeoutError):
            log('WARNING', 'MongoDB connection lost, reconnecting...', 
                category='database', action='reconnect')
            _client = None
            return _get_client()  # Recursive call to reconnect
    
    return _client


def _get_database() -> Database:
    """
    Get the application database.
    
    Returns:
        MongoDB Database instance
    """
    global _db, _db_name
    
    settings = load_user_settings()
    mongo_settings = settings.get('mongodb', {}) if isinstance(settings, dict) else {}

    database_name = mongo_settings.get('database')
    if isinstance(database_name, str):
        database_name = database_name.strip()
    database_name = database_name or os.getenv('MONGODB_DATABASE', DEFAULT_DATABASE_NAME)

    if _db is None or _db_name != database_name:
        client = _get_client()
        _db = client[database_name]
        _db_name = database_name
        log('INFO', f'Using database: {database_name}',
            category='database', action='get_database')
    
    return _db


# Collection access functions
# These are simple wrappers that establish connection on first use
def _get_collection(collection_name: str) -> Collection:
    """
    Get a collection from the database.
    
    Establishes database connection if not already connected.
    
    Args:
        collection_name: Name of the collection to retrieve
        
    Returns:
        MongoDB Collection instance
    """
    db = _get_database()
    return db[collection_name]


def get_stints_collection() -> Collection:
    """
    Get the stints collection.
    
    Stores stint data with schema:
    - driver: str (driver name)
    - laps: int (number of laps)
    - tire_compound: str (tire type)
    - start_time: datetime
    - end_time: datetime
    - session_id: ObjectId (reference to sessions)
    
    Returns:
        MongoDB Collection instance for stints
    """
    return _get_collection('stints')


def get_events_collection() -> Collection:
    """
    Get the events collection.
    
    Stores race events with schema:
    - name: str (event name)
    - track: str (track name)
    - date: datetime
    - season: str
    
    Returns:
        MongoDB Collection instance for events
    """
    return _get_collection('events')


def get_sessions_collection() -> Collection:
    """
    Get the sessions collection.
    
    Stores race sessions with schema:
    - name: str (session name)
    - event_id: ObjectId (reference to events)
    - type: str (practice/qualifying/race)
    - conditions: dict (weather, track temp, etc.)
    - start_time: datetime
    
    Returns:
        MongoDB Collection instance for sessions
    """
    return _get_collection('sessions')


def get_teams_collection() -> Collection:
    """
    Get the teams collection.
    
    Stores team data with schema:
    - name: str (team name)
    - drivers: list[str] (driver names)
    - car_info: dict (car details)
    
    Returns:
        MongoDB Collection instance for teams
    """
    return _get_collection('teams')


def get_strategies_collection() -> Collection:
    """
    Get the strategies collection.
    
    Stores race strategies with schema:
    - event_id: ObjectId (reference to events)
    - session_id: ObjectId (reference to sessions)
    - tire_allocation: dict (tire types and counts)
    - pit_windows: list[dict] (planned pit stops)
    - fuel_strategy: dict
    
    Returns:
        MongoDB Collection instance for strategies
    """
    return _get_collection('strategies')


# Convenience aliases for backward compatibility and easier imports
stints_col = get_stints_collection()
events_col = get_events_collection()
sessions_col = get_sessions_collection()
teams_col = get_teams_collection()
strategies_col = get_strategies_collection()


def close_connection() -> None:
    """
    Close the MongoDB connection.
    
    Should be called when the application is shutting down.
    """
    global _client, _db
    
    if _client is not None:
        try:
            _client.close()
            log('INFO', 'MongoDB connection closed', 
                category='database', action='close')
        except Exception as e:
            log_exception(e, 'Error closing MongoDB connection', 
                         category='database', action='close')
        finally:
            _client = None
            _db = None
