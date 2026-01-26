from helpers.db import stints_col

def update_stint(stint_id, tire_data):
  query = { "_id": stint_id }

  doc = { "$set":{
      "tire_data": tire_data
  }}

  stints_col.update_one(query, doc)