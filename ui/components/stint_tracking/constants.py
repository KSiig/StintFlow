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
    {"title": "Tires changed", "icon": "arrow-left-right.svg"},
    {"title": "Tires left", "icon": "life-buoy.svg"},
    {"title": "Stint time", "icon": "timer.svg"}
]

# Column widths (in pixels)
COLUMN_WIDTHS = {
    0: 104,   # Stint type
    1: 128,  # Driver
    2: 104,   # Status
    3: 128,  # Pit end time
    4: 128,   # Tires changed
    5: 96,   # Tires left
    6: 128,  # Stint time
    7: 128,  # Actions
}

# Vertical header (row numbers)
VERTICAL_HEADER_WIDTH = 90
VERTICAL_HEADER_LABEL = "Stint no."

# Table refresh interval (milliseconds)
# Disabled by default - use signal-based updates instead
REFRESH_INTERVAL_MS = 5000
