from helpers.db import *
from bson.objectid import ObjectId

def create_event(doc):
  return events_col.insert_one(doc)