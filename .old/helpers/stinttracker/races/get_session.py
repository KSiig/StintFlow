from helpers.db import *
from bson.objectid import ObjectId

def get_session(session_id):
  return sessions_col.find_one({"_id": ObjectId(session_id)})