from helpers.db import strategies_col

def update_strategy(strategy_id, model_data):
  query = { "_id": strategy_id }

  doc = { "$set":{
      "model_data": model_data
  }}

  strategies_col.update_one(query, doc)