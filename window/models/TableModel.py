from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from helpers.stinttracker import get_stints
from ..Fonts import FONT, get_fonts
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
import json
import copy

class TableModel(QAbstractTableModel):
    def __init__(self, selection_model, headers, data = []):
        super().__init__()
        self.selection_model = selection_model
        if data:
            self._data = data
        else:
            self.set_data()
        self.headers = headers
        self.editable = False

    def clone(self):
        return TableModel(
            selection_model=self.selection_model,
            headers=copy.deepcopy(self.headers),
            data=copy.deepcopy(self._data)
        )

    def update_data(self, data = ""):
        self.beginResetModel()
        self.set_data(data)
        self.endResetModel()
    
    def set_data(self, data = ""):
        if not data:
            event = get_event(self.selection_model.event_id)
            if event:
                tires = str(event['tires'])
                starting_time = event['length']
            else:
                tires = "0"
                starting_time = "00:00:00"
            
            stints = list(get_stints(self.selection_model.session_id))
            self._data = stints_to_table(stints, tires, starting_time)
            self.repaint_table()
        else:
            self._data = data
            self.repaint_table()

    def recalc_tires(self):
        event = get_event(self.selection_model.event_id)
        remaining_tires = event['tires']
        for row in self._data:
            tires_changed = row[3]
            row[4] = int(remaining_tires) - int(tires_changed)
            remaining_tires = row[4]

        self.repaint_table()

    
    def setData(self, index, value, role = Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        row, col = index.row(), index.column()

        # Update your underlying data
        self._data[row][col] = value

        # Notify the view that the cell has changed
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])

        return True

    def repaint_table(self):
        topLeft = self.index(0, 0)
        bottomRight = self.index(
            self.rowCount() - 1,
            self.columnCount() - 1
        )

        if self.rowCount() > 0 and self.columnCount() > 0:
            self.dataChanged.emit(topLeft, bottomRight, [])

    def set_editable(self, editable):
        self.editable = editable

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        if self.editable:
            return (
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsEditable
            )
        else:
            return Qt.ItemFlag.NoItemFlags

    def data(self, index, role):
        font_text_table_cell = get_fonts(FONT.text_table_cell)
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.FontRole:
            return font_text_table_cell

        if role == Qt.ItemDataRole.TextAlignmentRole:
        #   if index.column() == 1:
            return Qt.AlignmentFlag.AlignHCenter + Qt.AlignmentFlag.AlignVCenter

    def get_all_data(self):
        return self._data

    def rowCount(self, parent=QModelIndex()):
        # The `index` argument is not used for table models.
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        # The `index` argument is not used for table models.
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0]) if self._data else 0

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
              return self.headers[section]

            if orientation == Qt.Orientation.Vertical:
                    return section + 1