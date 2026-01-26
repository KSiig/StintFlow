from helpers.db import *
from bson import ObjectId

def update_drivers(team_id, drivers):
    query = { "_id": team_id }

    doc = { "$set":{
        "drivers": drivers
    }}

    teams_col.update_one(query, doc)