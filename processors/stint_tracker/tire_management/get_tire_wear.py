"""
Calculate tire wear from vehicle telemetry.

Determines wear percentage for individual tires.
"""

from typing import Any


# Tire position to wheel index mapping
TIRE_INDEX = {
    "fl": 0,
    "fr": 1,
    "rl": 2,
    "rr": 3
}


def get_tire_wear(player_vehicle: Any, tire_position: str) -> float:
    """
    Get wear percentage for a specific tire.
    
    Args:
        player_vehicle: LMU player vehicle telemetry object
        tire_position: Tire position ("fl", "fr", "rl", "rr")
        
    Returns:
        Wear value as float (1.0 = new, 0.0 = worn out)
    """
    wheel_idx = TIRE_INDEX.get(tire_position, 0)
    wheel = player_vehicle.mWheels[wheel_idx]
    
    return round(wheel.mWear, 2)
