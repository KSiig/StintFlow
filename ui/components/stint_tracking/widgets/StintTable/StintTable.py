"""Stint table component for displaying race stint data."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from ui.models import ModelContainer
from core.errors import log

from .helpers import (
    _create_table,
    _hide_placeholder,
    _load_stylesheet,
    _on_delete_clicked,
    _refresh_editors,
    _set_column_widths,
    _setup_corner_button,
    _setup_delegates,
    _setup_editors,
    _setup_horizontal_header,
    _setup_vertical_header,
    _show_placeholder,
    refresh_table,
)


class StintTable(QWidget):
    """Table view for displaying racing stint data."""

    ROW_PADDING_VERTICAL = 40
    CORNER_ICON_SIZE = 16
    CORNER_ICON_SPACING = 4
    CORNER_PADDING_LEFT = 8
    CORNER_PADDING_RIGHT = 4
    VERTICAL_HEADER_PADDING_LEFT = 12
    CORNER_HEIGHT_ADJUSTMENT = 26

    _load_stylesheet = _load_stylesheet
    _create_table = _create_table
    _setup_vertical_header = _setup_vertical_header
    _setup_horizontal_header = _setup_horizontal_header
    _setup_corner_button = _setup_corner_button
    _setup_delegates = _setup_delegates
    _on_delete_clicked = _on_delete_clicked
    _setup_editors = _setup_editors
    _refresh_editors = _refresh_editors
    refresh_table = refresh_table
    _show_placeholder = _show_placeholder
    _hide_placeholder = _hide_placeholder
    _set_column_widths = _set_column_widths

    def __init__(self, models: ModelContainer, focus: bool = False, auto_update: bool = True, allow_editors: bool = False, enable_actions: bool = False):
        super().__init__()

        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self._column_count = 0
        self._load_stylesheet()

        self.table = self._create_table(focus)

        table_frame = QFrame(self)
        table_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        table_frame.setObjectName("StintTableFrame")
        frame_layout = QHBoxLayout(table_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.table)

        container = QHBoxLayout(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.addWidget(table_frame)
        self._placeholder_label = QLabel("No stints found for the session, head to the config menu to get started!")
        self._placeholder_label.setObjectName("StintTablePlaceholder")
        self._placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder_label.setStyleSheet("color: #99A1AF; font-size: 16px; padding: 32px;")
        self._placeholder_label.hide()
        self._placeholder_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._placeholder_label.setMinimumWidth(self.table.minimumWidth())
        frame_layout.addWidget(self._placeholder_label, 1)

        if self.table_model is not None:
            self.table_model.update_data()
            self.refresh_table()
            self._setup_delegates()
            if allow_editors:
                self._setup_editors()
            else:
                self.table_model.editorsNeedRefresh.connect(self._refresh_editors)
        else:
            log('WARNING', 'TableModel not available - table will be empty', category='stint_table', action='init')

        if auto_update:
            self.selection_model.sessionChanged.connect(self.refresh_table)
