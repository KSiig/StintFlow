"""
Model container dataclass for passing models to UI components.

This provides type-safe, IDE-friendly model passing with clear dependencies.
"""

from dataclasses import dataclass


@dataclass
class ModelContainer:
    """
    Container for application models passed to UI components.
    
    All models are optional (default to None).
    Components should only access models they actually need.
    
    Attributes:
        selection_model: Shared selection state across components
        table_model: Table data model
        navigation_model: Navigation state model
    """
    selection_model: object = None
    table_model: object = None
    navigation_model: object = None
