from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from helpers.stinttracker import get_stints
from ..Fonts import FONT, get_fonts
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
import json
import copy
from .TableRoles import TableRoles

class TableModel(QAbstractTableModel):
    editorsNeedRefresh = pyqtSignal()
    def __init__(self, selection_model, headers, data = [], tires = [], meta = []):
        super().__init__()
        self.selection_model = selection_model
        if data:
            self._data = data
            self._tires = tires
            self._meta = meta
        else:
            self.set_data()
        self.headers = headers
        self.editable = False

    def clone(self):
        return TableModel(
            selection_model=self.selection_model,
            headers=copy.deepcopy(self.headers),
            data=copy.deepcopy(self._data),
            tires=copy.deepcopy(self._tires),
        )

    def update_data(self, data = "", tires = ""):
        self.beginResetModel()
        self.set_data(data, tires)
        self.endResetModel()
    
    def set_data(self, data = "", tires = ""):
        if not data:
            event = get_event(self.selection_model.event_id)
            if event:
                tires = str(event['tires'])
                starting_time = event['length']
            else:
                tires = "0"
                starting_time = "00:00:00"
            
            stints = list(get_stints(self.selection_model.session_id))
            self._tires = [stint["tire_data"] for stint in stints]
            self._meta = [
                {"id": stint["_id"]}
                for stint in stints
            ]
            self._data = stints_to_table(stints, tires, starting_time)
            for i, row in enumerate(self._data):
                if i >= len(self._tires):
                    self._tires.append(self.get_tire_dict(True))

            self.recalc_stint_types()
            self.repaint_table()
        else:
            self._data = data
            self._tires = tires
            self.repaint_table()

    def recalc_tires_left(self):
        event = get_event(self.selection_model.event_id)
        tires_left = int(event['tires'])
        for i, row in enumerate(self._data):

            for tire in ["fl", "fr", "rl", "rr"]:
                is_tire_changed = self._tires[i]['tires_changed'][tire]
                compound = self._tires[i][tire]['outgoing']['compound'].lower()

                if is_tire_changed and compound == 'medium':
                    tires_left -= 1
            row[5] = tires_left

        self.recalc_stint_types()

    def recalc_tires_changed(self, index, old_value):
        row = index.row()
        total_rows = self.rowCount()

        old_len = self.get_stint_len(old_value)
        new_len = self.get_stint_len(self._data[row][0])
        delta = new_len - old_len

        # Snapshot current tire changes
        old_tire_changes = [
            {"row": i, "value": self._data[i][4], "tires": self._tires[i]}
            for i in range(total_rows) if int(self._data[i][4]) > 0
        ]

        # Clear all tire changes (we'll rebuild)
        for r in range(total_rows):
            self._data[r][4] = "0"
            self._tires[r] = self.get_tire_dict(False)

        # Re-apply tire changes
        for tc in old_tire_changes:
            old_row = tc["row"]

            if row <= old_row < row + old_len:
                # Tire change belongs to the edited stint → move to new end of stint
                new_row = min(row + new_len - 1, total_rows - 1)
            elif old_row >= row + old_len:
                # Downstream tire change → shift by delta
                new_row = old_row + delta
            else:
                # Upstream → stays the same
                new_row = old_row

            # Only apply if within bounds
            if 0 <= new_row < total_rows:
                self._data[new_row][4] = tc["value"]
                self._tires[new_row] = tc["tires"]

        # Force tire change at the end of the edited stint
        forced_tc_row = min(row + new_len - 1, total_rows - 1)
        self._data[forced_tc_row][4] = "4"
        self._tires[forced_tc_row] = self.get_tire_dict(True)

        # Recalculate tires left
        self.recalc_tires_left()

    def get_tire_dict(self, tire_changed):
        return {
            "fr": {
                "incoming": {
                "wear": 0.95,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                },
                "outgoing": {
                "wear": 1,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                }
            },
            "fl": {
                "incoming": {
                "wear": 0.97,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                },
                "outgoing": {
                "wear": 1,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                }
            },
            "rl": {
                "incoming": {
                "wear": 0.94,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                },
                "outgoing": {
                "wear": 1,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                }
            },
            "rr": {
                "incoming": {
                "wear": 0.93,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                },
                "outgoing": {
                "wear": 1,
                "flat": False,
                "detached": False,
                "compound": "Medium"
                }
            },
            "tires_changed": {
                "fl": tire_changed,
                "fr": tire_changed,
                "rl": tire_changed,
                "rr": tire_changed
            }
        }

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
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1, 6),
            [Qt.ItemDataRole.DisplayRole, TableRoles.TiresRole]
        )
        self.repaint_table()
    
    def setData(self, index, value, role = Qt.ItemDataRole.EditRole):
        if not index.isValid() or role not in (
            Qt.ItemDataRole.EditRole,
            TableRoles.TiresRole,
        ):
            return False

        row, col = index.row(), index.column()

        if role == Qt.ItemDataRole.EditRole:
            # Update your underlying data
            self._data[row][col] = value

        elif role == TableRoles.TiresRole:
            self._tires[row] = value
            tires_changed = sum(value['tires_changed'].values())
            self._data[row][4] = tires_changed

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

    def set_editable(self, editable, partial = False):
        self.editable = editable
        self.partial = partial

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        status_index = self.index(index.row(), 2)
        status = self.data(status_index, Qt.ItemDataRole.DisplayRole)


        if self.editable and self.partial:
            if "Completed" in status:
                return (
                    Qt.ItemFlag.ItemIsSelectable |
                    Qt.ItemFlag.ItemIsEnabled |
                    Qt.ItemFlag.ItemIsEditable
                )
            else:
                return Qt.ItemFlag.NoItemFlags
        elif self.editable:
            return (
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsEditable
            )
        else:
            return Qt.ItemFlag.NoItemFlags

    def data(self, index, role):
        if not index.isValid():
            return None
        font_text_table_cell = get_fonts(FONT.text_table_cell)

        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.FontRole:
            return font_text_table_cell

        if role == TableRoles.MetaRole:
            return self._meta[row]

        if role == Qt.ItemDataRole.TextAlignmentRole:
        #   if index.column() == 1:
            return Qt.AlignmentFlag.AlignHCenter + Qt.AlignmentFlag.AlignVCenter

        if role == TableRoles.TiresRole:
            return self._tires[row]


    def get_all_data(self):
        return self._data, self._tires

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