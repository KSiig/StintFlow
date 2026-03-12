from datetime import timedelta
from typing import Tuple

from ._build_table_data_payload import _build_table_data_payload


def load_table_data(selection_model) -> Tuple[list, list, timedelta]:
    """Load stint data for the given selection."""
    payload = _build_table_data_payload(selection_model)
    if payload is None:
        return [], [], timedelta(0)

    return payload["rows"], payload["tires"], payload["mean_stint_time"]
