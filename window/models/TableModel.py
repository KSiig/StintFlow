from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from helpers.stinttracker import get_stints
from ..Fonts import FONT, get_fonts
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
import json
import copy

class TableModel(QAbstractTableModel):
    editorsNeedRefresh = pyqtSignal()
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

    def recalc_tires_left(self):
        event = get_event(self.selection_model.event_id)
        remaining_tires = event['tires']
        for row in self._data:
            tires_changed = row[4]
            row[5] = int(remaining_tires) - int(tires_changed)
            remaining_tires = row[5]

        self.recalc_stint_types()

    # def recalc_tires_changed(self, index, change_in_stints, old_value, diff_in_stints):
    #     row = index.row()
    #     next_row = row + 1

    #     print("change_in_stints", change_in_stints)

    #     old_column = [row[4] for row in self._data]
    #     total_rows = self.rowCount()

    #     if change_in_stints:
    #         if old_value == "Single":
    #             self._data[row][4] = "0"
    #         else:
    #             for i in range(change_in_stints):
    #                 print("i: ", i)
    #                 print("next_row: ", next_row)
    #                 print("old_value", old_value)
    #                 self._data[next_row + i][4] = "0"

    #     for i, row in enumerate(self._data):
    #         print(i, row[4])

    #     print("diff_in_stints: ", diff_in_stints)

    #     if diff_in_stints > 1:
    #         starting_range = next_row + diff_in_stints
    #     else:
    #         starting_range = next_row
    #     for i in range(starting_range, total_rows):
    #         src_index = i - change_in_stints + 1  # Where to copy from
    #         print("i: ", i)
    #         print("src_index: ", src_index)

    #         if 0 <= src_index < total_rows:
    #             # Shift value
    #             self._data[i][4] = old_column[src_index]
    #         else:
    #             # Out of bounds -> reset to "0"
    #             self._data[i][4] = "0"

    #     self.recalc_tires_left()

    def recalc_tires_changed(self, index, old_value):
        row = index.row()
        total_rows = self.rowCount()

        old_len = self.get_stint_len(old_value)
        new_len = self.get_stint_len(self._data[row][0])
        delta = new_len - old_len

        # 1. Snapshot existing tire change positions
        old_tc_rows = [
            i for i, r in enumerate(self._data)
            if int(r[4]) > 0
        ]

        # 2. Clear all tire changes
        for r in range(total_rows):
            self._data[r][4] = "0"

        # 3. Re-apply tire changes
        for tc_row in old_tc_rows:
            # Tire change belonging to edited stint → recompute
            if row <= tc_row < row + old_len:
                new_tc = min(row + new_len - 1, total_rows - 1)
            # Downstream tire change → shift
            elif tc_row >= row + old_len:
                new_tc = tc_row + delta
            # Upstream → untouched
            else:
                new_tc = tc_row

            if 0 <= new_tc < total_rows:
                self._data[new_tc][4] = "4"

        # 4. FORCE tire change for edited stint (this fixes last-stint issue)
        forced_tc = min(row + new_len - 1, total_rows - 1)
        self._data[forced_tc][4] = "4"

        self.recalc_tires_left()

    def get_stint_len(self, stint_type):
        if not stint_type:
            return 1
        mapping = {
            "Single": 1,
            "Double": 2,
            "Triple": 3,
            "Quadruple": 4,
            "Quintuple": 5,
            "Sextuple": 6,
            "Septuple": 7,
            "Octuple": 8,
            "Nonuple": 9,
            "Decuple": 10,
        }
        return mapping.get(stint_type, 1)

    def recalc_stint_types(self):
        start_of_stint = 0
        for i, row in enumerate(self._data):
            tires_changed = int(row[4])

            stint_amounts = i - start_of_stint
            stint_type = self.get_stint_type(stint_amounts + 1)

            if tires_changed:
                stint_type = ""
                if start_of_stint == i:
                    stint_type = "Single"
                start_of_stint = i + 1
            
            # If it's more than a double stint
            if stint_amounts and not tires_changed:
                self._data[start_of_stint][0] = self.get_stint_type(stint_amounts + 1)
                stint_type = ""

            row[0] = stint_type

        self.editorsNeedRefresh.emit()
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

    def get_stint_type(self, stint_amounts):
        match stint_amounts:
            case 0:
                return "Single"
            case 1:
                return "Double"
            case 2:
                return "Triple"
            case 3:
                return "Quadruple"
            case 4:
                return "Quintuple"
            case 5:
                return "Sextuple"
            case 6:
                return "Septuple"
            case 7:
                return "Octuple"
            case 8:
                return "Nonuple"
            case 9:
                return "Decuple"
            case _:
                return "Unknown"