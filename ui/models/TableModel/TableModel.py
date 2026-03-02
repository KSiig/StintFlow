from __future__ import annotations

from PyQt6.QtCore import QAbstractTableModel, pyqtSignal

from .bounded_functions._assemble_header_data import headerData
from .bounded_functions._clone import clone
from .bounded_functions._column_count import columnCount
from .bounded_functions._data import data
from .bounded_functions._delete_stint import delete_stint
from .bounded_functions._flags import flags
from .bounded_functions._get_all_data import get_all_data
from .bounded_functions._get_editable_flags import _get_editable_flags
from .bounded_functions._init_model import __init__
from .bounded_functions._load_data_from_database import _load_data_from_database
from .bounded_functions._parse_pit_time import _parse_pit_time
from .bounded_functions._recalculate_stint_types import _recalculate_stint_types
from .bounded_functions._recalculate_tires_changed import _recalculate_tires_changed
from .bounded_functions._recalculate_tires_left import _recalculate_tires_left
from .bounded_functions._repaint_table import _repaint_table
from .bounded_functions._row_count import rowCount
from .bounded_functions._set_data import setData
from .bounded_functions._set_editable import set_editable
from .bounded_functions._update_data import update_data
from .bounded_functions._update_mean import update_mean


class TableModel(QAbstractTableModel):
    """Model for stint tracking table data."""

    editorsNeedRefresh = pyqtSignal()

    __init__ = __init__
    clone = clone
    update_data = update_data
    _load_data_from_database = _load_data_from_database
    _recalculate_tires_left = _recalculate_tires_left
    _recalculate_tires_changed = _recalculate_tires_changed
    _recalculate_stint_types = _recalculate_stint_types
    _repaint_table = _repaint_table
    update_mean = update_mean
    _parse_pit_time = _parse_pit_time
    set_editable = set_editable
    get_all_data = get_all_data
    delete_stint = delete_stint
    rowCount = rowCount
    columnCount = columnCount
    data = data
    setData = setData
    flags = flags
    _get_editable_flags = _get_editable_flags
    headerData = headerData
