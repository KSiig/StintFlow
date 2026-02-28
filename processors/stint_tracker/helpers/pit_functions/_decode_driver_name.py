from typing import Any, Optional

from core.errors import log, log_exception

# Logging metadata constants to avoid repeated literals
_LOG_CATEGORY = 'stint_tracker'
_LOG_ACTION = 'find_player'

def _decode_driver_name(vehicle: Any, index: int) -> Optional[str]:
    """Safely extract and normalize a driver name from a vehicle record.

    Returns the trimmed string name on success, or ``None`` if the name
    cannot be decoded or is missing. All decoding/normalization concerns
    are isolated here.
    """
    raw = getattr(vehicle, 'mDriverName', None)
    if raw is None:
        return None

    # If the LMU struct provides bytes, decode; otherwise coerce to str
    if isinstance(raw, (bytes, bytearray)):
        try:
            return raw.decode('utf-8').strip()
        except UnicodeDecodeError as e:
            log('WARNING', f'Invalid UTF-8 for driver name at index {index}: {e}',
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            return None

    try:
        return str(raw).strip()
    except Exception as e:  # defensive: unexpected value type
        log_exception(e, 'Failed converting driver name to string',
                      category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None