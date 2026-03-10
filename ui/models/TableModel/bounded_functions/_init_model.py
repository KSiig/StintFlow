from __future__ import annotations

from datetime import timedelta
from PyQt6.QtCore import QAbstractTableModel

from ._load_data_from_database import _load_data_from_database


def __init__(
    self,
    selection_model,
    headers: list[dict],
    data: list[list] = None,
    tires: list[dict] = None,
    meta: list[dict] = None,
    mean_stint_time: timedelta = None,
    load_on_init: bool = True,
) -> None:
    """Initialize the table model."""
    QAbstractTableModel.__init__(self)

    self.selection_model = selection_model
    self.headers = headers
    self.editable = False
    self.partial = False
    self._event_tire_count = None

    if data is not None:
        self._data = data
        self._tires = tires or []
        self._meta = meta or []
        self._mean_stint_time = mean_stint_time or timedelta(0)
    else:
        self._data = []
        self._tires = []
        self._meta = []
        self._mean_stint_time = timedelta(0)
        if load_on_init:
            _load_data_from_database(self)
