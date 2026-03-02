"""Dataclass container for sharing models across UI components."""

from dataclasses import dataclass


@dataclass
class ModelContainer:
    """Container for application models passed to UI components."""

    selection_model: object = None
    table_model: object = None
    navigation_model: object = None
