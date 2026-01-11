from datetime import datetime, date
from .pits import *
from helpers.stinttracker import *
from helpers.stinttracker import *
from helpers.db import *
import math
import time

updating = False
num_penalties = 0
remaining_time_out_of_pits = "00:00:00"
recording = False
stints = []
prev_time = "00:00:00"
driver_name = ""

def update_stint(telemetry, scoring, tracking_data):
  global updating
  global player_names
  global num_penalties
  global remaining_time_out_of_pits
  global recording
  global stints
  global prev_time
  global driver_name

  is_practice = tracking_data['is_practice']


  # Find either length of event or latest `pit_end_time`
  if is_practice and not stints:
    stints = list(get_stints(tracking_data['session_id']))
    if stints:
      prev_time = stints[-1]['pit_end_time']
    else:
      session = get_session(tracking_data['session_id'])
      event = get_event(session['race_id'])
      prev_time = event['length']

  # Initialize player vehicle telemetry and scoring objects
  player_idx = telemetry.playerVehicleIdx
  player_vehicle = telemetry.telemInfo[player_idx]
  player_vehicle_scoring, driver_name_cur = find_scoring_vehicle(telemetry, scoring, tracking_data['drivers'])
  if get_pit_state(player_vehicle_scoring) == PITSTATE['coming_in'].value:
    driver_name = driver_name_cur
  tracking_data['driver_name'] = driver_name
      
  if is_practice and not recording:
    while not is_in_garage(player_vehicle_scoring):
      print('__info__:stint_tracker:return_to_garage')
      time.sleep(1)
    recording = True
  else:
    recording = True

  # Ensure a stint isn't recorded when leaving the garage
  if is_in_garage(player_vehicle_scoring):
    print("__info__:stint_tracker:player_in_garage")
    updating = True
    remaining_time_out_of_pits = get_remaining_time(scoring)
      
  # If pit stop has just ended, proceed to update
  if (not updating 
      and get_pit_state(player_vehicle_scoring) == PITSTATE['leaving'].value 
      ):
    updating = True

    if is_practice:
      actual_remaining_time = get_remaining_time(scoring)
      remaining_time = get_practice_time(prev_time, remaining_time_out_of_pits, actual_remaining_time)
    else:
       remaining_time = get_remaining_time(scoring)

    create_pit_stop(
      remaining_time, 
      player_vehicle,
      player_vehicle_scoring,
      num_penalties,
      tracking_data)
    
  if get_pit_state(player_vehicle_scoring) == PITSTATE['on_track'].value:
    num_penalties = player_vehicle_scoring.mNumPenalties
    updating = False

def get_remaining_time(scoring, start_time = "00:00:00", end_time = "00:00:00"):
  # Base remaining time from scoring
    d = math.ceil(
        scoring.scoringInfo.mEndET -
        scoring.scoringInfo.mCurrentET
    )

    # Convert inputs to seconds
    start_seconds = hhmmss_to_seconds(start_time)
    end_seconds = hhmmss_to_seconds(end_time)

    # Apply calculation
    total_seconds = d + end_seconds - start_seconds

    return seconds_to_hhmmss(total_seconds)
  
def hhmmss_to_seconds(t: str) -> int:
  h, m, s = map(int, t.split(":"))
  return h * 3600 + m * 60 + s


def seconds_to_hhmmss(seconds: int) -> str:
    seconds = max(0, seconds)  # avoid negative time
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def get_practice_time(prev_time, start_time, end_time):
    # Convert inputs to seconds
    prev_seconds = hhmmss_to_seconds(prev_time)
    start_seconds = hhmmss_to_seconds(start_time)
    end_seconds = hhmmss_to_seconds(end_time)

    # Apply calculation
    total_seconds = prev_seconds + end_seconds - start_seconds

    return seconds_to_hhmmss(total_seconds)