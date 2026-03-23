"""
Constants for stint tracking components.

Configuration values for table display, column widths, and styling.
"""

# Table headers with icons
TABLE_HEADERS = [
    {"title": "Stint type", "icon": "list.svg"},
    {"title": "Driver", "icon": "user.svg"},
    {"title": "Status", "icon": "circle.svg"},
    {"title": "Pit end time", "icon": "clock.svg"},
    {"title": "Changed", "icon": "life-buoy.svg"},
    {"title": "Left", "icon": "life-buoy.svg"},
    {"title": "Stint time", "icon": "timer.svg"},
    {"title": "Time of day", "icon": "clock.svg"}
]

# Column widths (in pixels)
COLUMN_WIDTHS = {
    0: 124,   # Stint type
    1: 154,  # Driver
    2: 120,   # Status
    3: 140,  # Pit end time
    4: 104,   # Changed
    5: 104,   # Left
    6: 128,  # Stint time
    7: 128,  # Time of day
    8: 128,  # Actions
}

# Vertical header (row numbers)
VERTICAL_HEADER_WIDTH = 64
VERTICAL_HEADER_LABEL = "No."

# Table refresh interval (milliseconds)
# Disabled by default - use signal-based updates instead
REFRESH_INTERVAL_MS = 5000
