from helpers.db import strategies_col

def create_strategy(strategy):
  strategies_col.insert_one(strategy)