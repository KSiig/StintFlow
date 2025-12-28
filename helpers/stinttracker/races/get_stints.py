from helpers.db import *
from bson.objectid import ObjectId

def get_stints(session_id):
  return stints_col.find({"session_id": ObjectId(session_id)})