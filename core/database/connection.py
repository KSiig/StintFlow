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


# MongoDB connection configuration
MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost:27017')
DATABASE_NAME = os.getenv('MONGODB_DATABASE', 'stintflow')
CONNECTION_TIMEOUT_MS = 5000  # 5 seconds
SERVER_SELECTION_TIMEOUT_MS = 5000  # 5 seconds
MAX_POOL_SIZE = 10  # Suitable for desktop application

# Global MongoDB client (initialized once)
_client: MongoClient | None = None
_db: Database | None = None


def _validate_host(host: str) -> bool:
    """
    Validate MongoDB host string format.
    
    Args:
        host: MongoDB host string (e.g., 'localhost:27017')
        
    Returns:
        True if valid, False otherwise
    """
    if not host or ':' not in host:
        return False
    
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
    global _client
    
    # Validate host format
    if not _validate_host(MONGODB_HOST):
        error_msg = f'Invalid MongoDB host format: {MONGODB_HOST} (expected format: hostname:port)'
        log('ERROR', error_msg, category='database', action='validate_host')
        raise ValueError(error_msg)
    
    # Create new client if none exists or test existing connection
    if _client is None:
        try:
            log('INFO', f'Connecting to MongoDB at {MONGODB_HOST}', 
                category='database', action='connect')
            
            _client = MongoClient(
                MONGODB_HOST,
                connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                maxPoolSize=MAX_POOL_SIZE
            )
            
            # Test the connection
            _client.server_info()
            log('INFO', 'MongoDB connection established', 
                category='database', action='connect')
                
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            log_exception(e, f'Failed to connect to MongoDB at {MONGODB_HOST}', 
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
    global _db
    
    if _db is None:
        client = _get_client()
        _db = client[DATABASE_NAME]
        log('INFO', f'Using database: {DATABASE_NAME}', 
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
