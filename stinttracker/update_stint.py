from datetime import datetime, date
from .pits import *
from helpers.stinttracker import *
from helpers.db import *
import math

updating = False
num_penalties = 0

def update_stint(telemetry, scoring, tracking_data):
  global updating
  global player_names
  global num_penalties

  # Initialize player vehicle telemetry and scoring objects
  player_idx = telemetry.playerVehicleIdx
  player_vehicle = telemetry.telemInfo[player_idx]
  player_vehicle_scoring = find_scoring_vehicle(telemetry, scoring, tracking_data['drivers'])
      
  # Ensure a stint isn't recorded when leaving the garage
  if is_in_garage(player_vehicle_scoring):
    updating = True
      
  # If pit stop has just ended, proceed to update
  if (not updating 
      and get_pit_state(player_vehicle_scoring) == PITSTATE['leaving'].value 
      ):
    updating = True
    create_pit_stop(
      get_remaining_time(scoring), 
      player_vehicle,
      player_vehicle_scoring,
      num_penalties,
      tracking_data)
    
  if get_pit_state(player_vehicle_scoring) == PITSTATE['on_track'].value:
    num_penalties = player_vehicle_scoring.mNumPenalties
    updating = False

def get_remaining_time(scoring):
  d = math.ceil(scoring.scoringInfo.mEndET - scoring.scoringInfo.mCurrentET)
  h = d // 3600
  m = (d % 3600) // 60
  s = d % 60

  return f"{h:02}.{m:02}.{s:02}"
  