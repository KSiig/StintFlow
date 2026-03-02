from datetime import timedelta


def update_data(self, data: list[list] = None, tires: list[dict] = None, mean_stint_time: timedelta = None) -> None:
    """Update model data and trigger view refresh."""
    self.beginResetModel()

    if data is not None:
        self._data = data
        self._tires = tires or []
        self._mean_stint_time = mean_stint_time or timedelta(0)
        self._repaint_table()
    else:
        self._load_data_from_database()

    self.endResetModel()
