"""
Constants for stint tracking components.

Configuration values for table display, column widths, and styling.
"""

# Table headers
TABLE_HEADERS = [
    "Stint type",
    "Driver",
    "Status",
    "Pit end time",
    "Tires changed",
    "Tires left",
    "Stint time"
]

# Column widths (in pixels)
COLUMN_WIDTHS = {
    0: 96,   # Stint type
    1: 200,  # Driver
    2: 96,   # Status
    3: 128,  # Pit end time
    4: 96,   # Tires changed
    5: 96,   # Tires left
    6: 128,  # Stint time
}

# Vertical header (row numbers)
VERTICAL_HEADER_WIDTH = 80
VERTICAL_HEADER_LABEL = "Stint no."

# Table refresh interval (milliseconds)
# Disabled by default - use signal-based updates instead
REFRESH_INTERVAL_MS = 5000
