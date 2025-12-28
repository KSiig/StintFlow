from helpers.db import *

def get_active_event():
  return events_col.find_one()