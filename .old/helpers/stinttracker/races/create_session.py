from helpers.db import *

def create_session(doc):
  return sessions_col.insert_one(doc)