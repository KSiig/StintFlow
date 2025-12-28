from helpers.db import *

def get_active_session():
  return sessions_col.find_one()