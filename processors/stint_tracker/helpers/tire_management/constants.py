"""Tire-management constants and lightweight helpers.

This module centralises small, well-documented constants used by the
stint-tracker tire-management code. Types are annotated to improve
readability and to make static analysis / testing easier.
"""

from typing import Dict, Mapping, Tuple

__all__ = [
    "TIRE_POSITIONS",
    "TIRE_INDEX_MAP",
    "COMPOUND_MAP",
    "WEAR_COMPARISON_EPSILON",
]


# Tire positions in canonical order: front-left, front-right, rear-left, rear-right
TIRE_POSITIONS: Tuple[str, ...] = ("fl", "fr", "rl", "rr")

# Mapping from short position code to wheel index (0..3)
TIRE_INDEX_MAP: Mapping[str, int] = {
    "fl": 0,  # front left
    "fr": 1,  # front right
    "rl": 2,  # rear left
    "rr": 3,  # rear right
}


# Compound mapping from LMU compound index to a human-friendly name.
# Keep this small; processors can extend or override if LMU provides
# additional compound indices for specific series or updates.
COMPOUND_MAP: Dict[int, str] = {
    0: "Medium",
    1: "Wet",
}


# Small epsilon for comparing floating-point tire-wear values
WEAR_COMPARISON_EPSILON: float = 0.01
