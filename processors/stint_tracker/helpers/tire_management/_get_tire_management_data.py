"""Retrieve tyre-management payload from the local LMU REST API.

This helper performs a short HTTP GET against the LMU local REST
endpoint that exposes tyre-management UI state. It returns the parsed
JSON object on success or ``None`` when the data cannot be retrieved.
"""

from typing import Any

import requests

from core.errors import log, log_exception

# LMU local REST endpoint and a conservative timeout to keep the tracker
# responsive when LMU is not available.
_LMU_TIRE_MGMT_URL = "http://localhost:6397/rest/garage/UIScreen/TireManagement"
_REQUEST_TIMEOUT_SECONDS = 2
_REQUEST_HEADERS = {"accept": "application/json"}


def _get_tire_management_data() -> Any | None:
    """Return LMU tyre-management JSON or ``None`` on failure.

    The function logs a DEBUG message on success and warning/error messages
    on failure. It intentionally keeps failures non-fatal; callers should
    be prepared to receive ``None`` and handle it gracefully.
    """
    try:
        resp = requests.get(_LMU_TIRE_MGMT_URL, headers=_REQUEST_HEADERS, timeout=_REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()

        data = resp.json()
        log('DEBUG', 'Successfully retrieved tire management data',
            category='stint_tracker', action='get_tire_management_data')
        return data

    except requests.RequestException as e:
        log('WARNING', f'Failed to retrieve tire management data: {e}',
            category='stint_tracker', action='get_tire_management_data')
        return None
    except ValueError as e:  # JSON decode error
        log('WARNING', f'Invalid JSON in tire management response: {e}',
            category='stint_tracker', action='get_tire_management_data')
        return None
    except Exception as e:
        log_exception(e, 'Unexpected error retrieving tire management data',
                     category='stint_tracker', action='get_tire_management_data')
        return None