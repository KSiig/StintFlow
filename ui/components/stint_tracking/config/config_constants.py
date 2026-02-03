"""
Constants for configuration options component.

Defines layout constants, button labels, and stint tracker event types.
"""


class StintTrackerEvents:
    """Constants for stint tracker event messages."""
    STINT_CREATED = 'stint_created'
    RETURN_TO_GARAGE = 'return_to_garage'
    PLAYER_IN_GARAGE = 'player_in_garage'


class ConfigLayout:
    """Layout and sizing constants for configuration options."""
    
    # Frame dimensions
    FRAME_WIDTH = 300
    ICON_SIZE = 20
    INPUT_HEIGHT = 40
    BTN_HEIGHT = 40
    RIGHT_MARGIN = 16
    
    # Spacing
    HEADER_SPACING = 8
    CONTENT_SPACING = 16
    BUTTON_SPACING = 8
    DRIVER_SPACING = 8
    ROW_SPACING = 8
    
    # Button width types (usable width = FRAME_WIDTH - RIGHT_MARGIN = 284)
    BTN_WIDTH_THIRD = 84   # Approximately 1/3 of usable width (accounting for spacing)
    BTN_WIDTH_HALF = 134   # Approximately 1/2 of usable width (accounting for spacing)
    BTN_WIDTH_FULL = 266   # Full usable width


class ConfigLabels:
    """Button and label text constants."""
    
    BTN_EDIT = "Edit"
    BTN_SAVE = "Save"
    BTN_CLONE = "Clone"
    BTN_NEW_SESSION = "+ New session"
    BTN_START_TRACK = "Track"
    BTN_STOP_TRACK = "Stop"
