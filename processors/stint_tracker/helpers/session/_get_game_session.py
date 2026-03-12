"""Resolve the current LMU game session from the local navigation API.

This helper performs a short HTTP GET against LMU's local navigation
endpoint and normalizes ``state.gameSession`` into a ``GAME_SESSION``
member. The suffix digits used by LMU are ignored intentionally so values
like ``PRACTICE1`` and ``RACE1`` map to stable session categories.
"""

import requests

from core.errors import log, log_exception

from .GAME_SESSION import GAME_SESSION

_LMU_NAVIGATION_STATE_URL = "http://localhost:6397/navigation/state"
_REQUEST_TIMEOUT_SECONDS = 2
_REQUEST_HEADERS = {"accept": "application/json"}


def _get_game_session() -> GAME_SESSION:
    """Return the normalized LMU game session.

    The function never raises for request or payload issues. Instead it
    logs the failure and returns ``GAME_SESSION.UNKNOWN`` so callers can
    degrade gracefully when LMU is unavailable or returns an unexpected
    payload.
    """
    try:
        resp = requests.get(
            _LMU_NAVIGATION_STATE_URL,
            headers=_REQUEST_HEADERS,
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()

        data = resp.json()
        state = data.get("state", {})
        nav_state = state.get("navigationState", "")

        # if we're not inside an event/realtime session, the session field is meaningless
        if nav_state not in ("NAV_EVENT", "NAV_REALTIME"):
            # only explicitly check menu - other navigation states could exist
            if nav_state == "NAV_MAIN_MENU":
                log(
                    "DEBUG",
                    "Navigation state indicates main menu, returning MENU session",
                    category="stint_tracker",
                    action="get_game_session",
                )
                return GAME_SESSION.MENU

            log(
                "DEBUG",
                f"Navigation state '{nav_state}' not in an event; treating as MENU",
                category="stint_tracker",
                action="get_game_session",
            )
            return GAME_SESSION.MENU

        raw_game_session = state.get("gameSession", "")

        if not isinstance(raw_game_session, str) or not raw_game_session.strip():
            log(
                "WARNING",
                "Navigation state did not include a valid gameSession value",
                category="stint_tracker",
                action="get_game_session",
            )
            return GAME_SESSION.UNKNOWN

        normalized_game_session = raw_game_session.casefold()

        if "practice" in normalized_game_session:
            log(
                "DEBUG",
                f"Resolved LMU game session '{raw_game_session}' to PRACTICE",
                category="stint_tracker",
                action="get_game_session",
            )
            return GAME_SESSION.PRACTICE

        if "qualify" in normalized_game_session:
            log(
                "DEBUG",
                f"Resolved LMU game session '{raw_game_session}' to QUALIFYING",
                category="stint_tracker",
                action="get_game_session",
            )
            return GAME_SESSION.QUALIFYING

        if "race" in normalized_game_session:
            log(
                "DEBUG",
                f"Resolved LMU game session '{raw_game_session}' to RACE",
                category="stint_tracker",
                action="get_game_session",
            )
            return GAME_SESSION.RACE

        log(
            "WARNING",
            f"Unrecognized LMU game session value: {raw_game_session}",
            category="stint_tracker",
            action="get_game_session",
        )
        return GAME_SESSION.UNKNOWN

    except requests.RequestException as e:
        log(
            "WARNING",
            f"Failed to retrieve game session data: {e}",
            category="stint_tracker",
            action="get_game_session",
        )
        return GAME_SESSION.UNKNOWN
    except ValueError as e:
        log(
            "WARNING",
            f"Invalid JSON in game session response: {e}",
            category="stint_tracker",
            action="get_game_session",
        )
        return GAME_SESSION.UNKNOWN
    except Exception as e:
        log_exception(
            e,
            "Unexpected error retrieving game session data",
            category="stint_tracker",
            action="get_game_session",
        )
        return GAME_SESSION.UNKNOWN
