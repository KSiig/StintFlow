def find_scoring_vehicle(telemetry, scoring, player_names):
  for i in range(telemetry.activeVehicles):
    vehicle = scoring.vehScoringInfo[i]

    driver_name = vehicle.mDriverName.decode()
    if driver_name in player_names:
      return vehicle, driver_name