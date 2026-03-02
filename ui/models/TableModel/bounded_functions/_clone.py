from __future__ import annotations

import copy


def clone(self) -> "TableModel":
    """Create a deep copy of this model."""
    from ui.models.TableModel import TableModel

    return TableModel(
        selection_model=self.selection_model,
        headers=copy.deepcopy(self.headers),
        data=copy.deepcopy(self._data),
        tires=copy.deepcopy(self._tires),
        meta=copy.deepcopy(self._meta),
        mean_stint_time=copy.deepcopy(self._mean_stint_time),
    )
