"""Barrel file for stint tracking components.

Views and components related to stint tracking functionality.

Directory Structure:
-------------------
views/      - Top-level view compositions (TrackerView)
widgets/    - Reusable widget components (ConfigOptions, StintTable)
delegates/  - Table cell renderers (DriverPillDelegate, StatusDelegate)
config/     - Configuration panel helpers (constants, UI builders, process handlers)
table/      - Table utilities (header views, icon/title helpers)
constants.py - Shared constants used across multiple modules
"""

# Views - main UI compositions
from .views import TrackerView, StrategiesView

# Widgets - reusable components
from .widgets import ConfigOptions, StintTable, AgentOverview, TeamSection

# Delegates - table cell renderers
from .delegates import DriverPillDelegate, StatusDelegate, TireComboDelegate, StintTypeCombo

# Config helpers - configuration panel utilities
from .config import (
    StintTrackerEvents, ConfigLayout, ConfigLabels,
    create_config_label,
    handle_stint_tracker_output
)

# Table helpers - table presentation utilities
from .table import SpacedHeaderView, get_header_icon, get_header_titles

__all__ = [
    # Views
    'TrackerView',
    'StrategiesView',
    
    # Widgets
    'ConfigOptions',
    'StintTable',
    'AgentOverview',
    'TeamSection',
    
    # Delegates
    'DriverPillDelegate',
    'StatusDelegate',
    'TireComboDelegate',
    'StintTypeCombo',
    
    # Config
    'StintTrackerEvents',
    'ConfigLayout',
    'ConfigLabels',
    'create_config_label',
    'handle_stint_tracker_output',
    
    # Table
    'SpacedHeaderView',
    'get_header_icon',
    'get_header_titles'
]