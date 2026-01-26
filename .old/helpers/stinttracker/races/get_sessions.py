from helpers.db import *
from bson.objectid import ObjectId

def get_sessions(event):
  return sessions_col.find({"race_id": ObjectId(event)})