"""Normalized game-session values for the stint tracker.

The LMU navigation API exposes session identifiers such as ``PRACTICE1``
or ``QUALIFY1``. This enum provides a stable set of session categories so
the rest of the tracker does not depend on LMU's exact suffix format.
"""

from enum import Enum


class GAME_SESSION(Enum):
    """Normalized game-session categories returned by LMU."""

    PRACTICE = "practice"
    QUALIFYING = "qualifying"
    RACE = "race"
    MENU = "menu"
    UNKNOWN = "unknown"