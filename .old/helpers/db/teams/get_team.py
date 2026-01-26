from helpers.db import *

def get_team():
  team = teams_col.find_one()

  return team