from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from helpers.stinttracker import get_stints

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self.headers = headers

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        
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