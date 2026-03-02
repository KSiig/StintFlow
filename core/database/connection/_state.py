"""Shared runtime state for MongoDB connection and database handle."""

from pymongo import MongoClient
from pymongo.database import Database

client: MongoClient | None = None
db: Database | None = None
db_name: str | None = None
client_config: dict | None = None
