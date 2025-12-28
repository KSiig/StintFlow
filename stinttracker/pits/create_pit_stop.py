from datetime import datetime
from helpers.stinttracker import *
from helpers.db import *
from ..tires import *
from ..pits import *
from bson.objectid import ObjectId

def create_pit_stop(remaining_time, vehicle, vehicle_scoring, num_penalties, tracking_data):

  is_penalty_served = num_penalties > vehicle_scoring.mNumPenalties

  tires = {
      "fl": get_tire_wear(vehicle, "fl"),
      "fr": get_tire_wear(vehicle, "fr"),
      "rl": get_tire_wear(vehicle, "rl"),
      "rr": get_tire_wear(vehicle, "rr")
    }
  tires_new = is_tires_new(tires)

  pitstop = {
    "session_id": ObjectId(tracking_data['session_id']),
    "driver": 'Kasper Siig',
    "pit_end_time": remaining_time,
    "tires_new": tires_new,
    "tires_changed": count_tires_changed(tires_new)
  }

  if not is_penalty_served:
    stints_col.insert_one(pitstop)
    print("Stint created")

  print("DONE")
