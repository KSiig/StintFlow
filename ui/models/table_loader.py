"""
Helper for loading stint table data outside of the TableModel class.

This module contains a single function that mirrors the logic previously
embedded in ``TableModel._load_data_from_database``.  Extracting it allows the
costly database query and conversion to be performed in a background thread
while the model itself is constructed on the main thread.
"""

from datetime import timedelta
from typing import Tuple

from core.database import get_event, get_stints
from core.errors import log

from .table_processors import convert_stints_to_table, count_tire_changes
from .table_constants import NO_TIRE_CHANGE
from .stint_helpers import get_default_tire_dict

# keep the same defaults that TableModel historically used, defined here to
# avoid a circular import.
DEFAULT_TIRE_COUNT = "0"
DEFAULT_RACE_LENGTH = "00:00:00"
DEFAULT_START_TIME = "00:00:00"


def load_table_data(selection_model) -> Tuple[list, list, timedelta]:
    """Load stint data for the given selection.

    Args:
        selection_model: SelectionModel with ``event_id`` and ``session_id``

    Returns:
        Tuple of (rows, tires, mean_stint_time).
    """
    # validate selection
    if not selection_model.event_id or not selection_model.session_id:
        log('WARNING', 'No event or session selected - cannot load table data',
            category='table_model', action='load_data')
        return [], [], timedelta(0)

    # get event info for tire count and race length
    event = get_event(selection_model.event_id)
    if event:
        total_tires = str(event.get('tires', DEFAULT_TIRE_COUNT))
        race_length = event.get('length', DEFAULT_RACE_LENGTH)
        start_time = event.get('start_time', DEFAULT_START_TIME)
    else:
        total_tires = DEFAULT_TIRE_COUNT
        race_length = DEFAULT_RACE_LENGTH
        start_time = DEFAULT_START_TIME
        log('WARNING', f'Event {selection_model.event_id} not found - using defaults',
            category='table_model', action='load_data')

    # get stints for current session
    stints = get_stints(selection_model.session_id)
    stints = sorted(stints, key=lambda s: s.get('pit_time', None) or 0, reverse=True)

    # extract tire and meta data
    tires = [stint.get("tire_data", {}) for stint in stints]

    # convert stints to table rows using existing processor
    rows, mean_stint_time, last_tire_change = convert_stints_to_table(
        stints, total_tires, race_length, count_tire_changes, start_time
    )

    # ensure tires array matches rows length
    i = 0 if last_tire_change is NO_TIRE_CHANGE else 1
    while len(tires) < len(rows):
        tires_changed = bool(i % 2)  # alternate between no change and full change
        tires.append(get_default_tire_dict(not tires_changed))
        i += 1

    return rows, tires, mean_stint_time
