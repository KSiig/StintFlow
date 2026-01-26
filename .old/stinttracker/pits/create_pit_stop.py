from datetime import datetime
from helpers.stinttracker import *
from helpers.db import *
from ..tires import *
from ..pits import *
from bson.objectid import ObjectId

def create_pit_stop(remaining_time, vehicle, vehicle_scoring, num_penalties, tracking_data):

  is_penalty_served = num_penalties > vehicle_scoring.mNumPenalties
  tire_mgmt_data = tracking_data['tire_mgmt_data']

  tire_data = {}
  for i, tire in enumerate(["fr", "fl", "rl", "rr"]):
    incoming = tracking_data['tires_coming_in'][tire]
    outgoing = {
        "wear": get_tire_wear(vehicle, tire),
        "flat": vehicle.mWheels[i].mFlat,
        "detached": vehicle.mWheels[i].mDetached,
        "compound": get_tire_compound(tire, tire_mgmt_data)
      }
    tire_data[tire] = {
      "incoming": incoming,
      "outgoing": outgoing
      
    }
  tire_data['tires_changed'] = is_tires_new({
      "fl": tire_data['fl']['outgoing']['wear'],
      "fr": tire_data['fr']['outgoing']['wear'],
      "rl": tire_data['rl']['outgoing']['wear'],
      "rr": tire_data['rr']['outgoing']['wear'],
    })


  pitstop = {
    "session_id": ObjectId(tracking_data['session_id']),
    "driver": tracking_data['driver_name'],
    "pit_end_time": remaining_time,
    "tire_data": tire_data,
  }

  if not is_penalty_served:
    stints_col.insert_one(pitstop)
    print("__event__:stint_tracker:stint_created")

