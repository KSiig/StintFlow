"""Update model data and trigger view refresh."""

from datetime import timedelta


def update_data(self, data: list[list] = None, tires: list[dict] = None, mean_stint_time: timedelta = None) -> None:
    """Update model data and trigger view refresh."""
    if data is not None:
        existing_row_count = len(self._data)
        new_row_count = len(data)

        if existing_row_count == new_row_count:
            self._data = data
            self._tires = tires or []
            self._mean_stint_time = mean_stint_time or timedelta(0)
            self._repaint_table()
            return

    self.beginResetModel()

    if data is not None:
        self._data = data
        self._tires = tires or []
        self._mean_stint_time = mean_stint_time or timedelta(0)
        self._repaint_table()
    else:
        self._load_data_from_database()

    self.endResetModel()
