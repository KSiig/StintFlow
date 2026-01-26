from enum import Enum

class PITSTATE(Enum):
  on_track = 0 # is also 0 when driver has joined server, but not started driving yet
  coming_in = 2
  pitting = 4
  leaving = 5

def get_pit_state(vehicle):
  return vehicle.mPitState

