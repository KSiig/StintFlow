from helpers.stinttracker.races import *

def is_tires_new(tires):
  return {
    "fl": tires['fl'] == 1.00,
    "fr": tires['fr'] == 1.00,
    "rl": tires['rl'] == 1.00,
    "rr": tires['rr'] == 1.00
  }