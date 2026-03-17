"""Driver names configuration section."""

from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QSizePolicy, QVBoxLayout, QWidget
from ui.utilities import FONT, get_fonts
from ui.components.common.ConfigButton import ConfigButton

from ...config import ConfigLayout, create_config_label
from .helpers import _add_row, _clear_drivers, _fetch_drivers, _load_team, _remove_row


class TeamSection(QWidget):
    """Widget for driver name inputs with add/remove controls."""

    _add_row = _add_row
    _clear_drivers = _clear_drivers
    _fetch_drivers = _fetch_drivers
    _load_team = _load_team
    _remove_row = _remove_row

    def __init__(self, parent=None, on_change=None):
        super().__init__(parent)
        self.setObjectName("DriverNames")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)
        self.on_change = on_change

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)
        title_label = create_config_label("Driver names")
        title_row.addWidget(title_label)
        title_row.addStretch(1)
        self.btn_add = ConfigButton("", icon_path="resources/icons/race_config/plus.svg", width="content", icon_size=16)
        self.btn_remove = ConfigButton("", icon_path="resources/icons/race_config/minus.svg", width="content", icon_size=16)
        self.btn_fetch = ConfigButton("", icon_path="resources/icons/race_config/cloud-sync.svg", width="content", icon_size=16)
        self.btn_add.clicked.connect(self._add_row)
        self.btn_remove.clicked.connect(self._remove_row)
        self.btn_fetch.clicked.connect(self._fetch_drivers)

        title_row.addWidget(self.btn_add)
        title_row.addWidget(self.btn_remove)
        title_row.addWidget(self.btn_fetch)

        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.setSpacing(8)
        main_box.addLayout(title_row)

        self.driver_box = QVBoxLayout()
        self.driver_box.setSpacing(ConfigLayout.DRIVER_SPACING)
        main_box.addLayout(self.driver_box)

        self.driver_inputs: list[QLineEdit] = []
        self.drivers: list[str] = []
        self._load_team()

    def get_driver_inputs(self):
        """Return driver input widgets."""
        return self.driver_inputs

    def get_driver_names(self):
        """Return driver names."""
        return self.drivers
