from helpers.db import *
from bson.objectid import ObjectId

def get_event(event_id):
  return events_col.find_one({"_id": ObjectId(event_id)})