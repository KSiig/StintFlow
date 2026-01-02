from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from helpers.stinttracker import get_stints
from ..Fonts import FONT, get_fonts
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path

class TableModel(QAbstractTableModel):
    def __init__(self, selection_model, headers):
        super().__init__()
        self.selection_model = selection_model
        self.set_data()
        self.headers = headers

    def update_data(self):
        self.beginResetModel()
        self.set_data()
        self.endResetModel()
    
    def set_data(self):
        event = get_event(self.selection_model.event_id)
        if event:
            tires = str(event['tires'])
            starting_time = event['length']
        else:
            tires = "0"
            starting_time = "00:00:00"
        
        stints = list(get_stints(self.selection_model.session_id))
        self._data = stints_to_table(stints, tires, starting_time)

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

    def rowCount(self, index):
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