from helpers.db import *

def get_events():
  return events_col.find()