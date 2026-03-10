from __future__ import annotations

from typing import TYPE_CHECKING

import copy


if TYPE_CHECKING:
    from ui.models.TableModel import TableModel


def clone(self) -> TableModel:
    """Create a deep copy of this model."""

    from ui.models.TableModel import TableModel as TableModelClass

    cloned_model = TableModelClass(
        selection_model=self.selection_model,
        headers=copy.deepcopy(self.headers),
        data=copy.deepcopy(self._data),
        tires=copy.deepcopy(self._tires),
        meta=copy.deepcopy(self._meta),
        mean_stint_time=copy.deepcopy(self._mean_stint_time),
    )

    cloned_model._event_tire_count = copy.deepcopy(self._event_tire_count)
    return cloned_model
