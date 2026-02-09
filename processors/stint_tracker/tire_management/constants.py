"""
Tire management constants.

Shared constants for tire-related operations.
"""

# All tire positions in order (front-left, front-right, rear-left, rear-right)
TIRE_POSITIONS = ["fl", "fr", "rl", "rr"]
# Map tire position to wheel index
TIRE_INDEX_MAP = {
    "fl": 0,  # Front left
    "fr": 1,  # Front right
    "rl": 2,  # Rear left
    "rr": 3   # Rear right
}

# Map compound index to compound name
# Note: This mapping is based on available LMU data and may be incomplete
COMPOUND_MAP = {
    0: "Medium",
    1: "Wet"
}
# Wear value threshold for detecting new tires
# Tires with wear >= this value are considered new
NEW_TIRE_THRESHOLD = 0.99

# Float comparison tolerance for tire wear values
WEAR_COMPARISON_EPSILON = 0.01
