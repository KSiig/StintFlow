from .get_tire_index import *

def get_tire_wear(vehicle, tire):
  return round(vehicle.mWheels[get_tire_index(tire)].mWear, 2)