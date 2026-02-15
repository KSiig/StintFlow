"""
TeamSection widget for driver names configuration.

Displays a section with driver name input fields and add/remove buttons.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QSizePolicy, QHBoxLayout
from ui.utilities import get_fonts, FONT
from core.database import get_team
from ..config.create_config_label import create_config_label
from ..config.config_constants import ConfigLayout
from ui.components.common import ConfigButton, PopUp

class TeamSection(QWidget):
    """
    QWidget for the driver names configuration section.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DriverNames")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)

        # Title row: label (left), buttons (right)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)
        title_label = create_config_label("Driver names")
        title_row.addWidget(title_label)
        title_row.addStretch(1)
        self.btn_add = ConfigButton("", icon_path="resources/icons/race_config/plus.svg", width_type="min", icon_size=16)
        self.btn_remove = ConfigButton("", icon_path="resources/icons/race_config/minus.svg", width_type="min", icon_size=16)
        self.btn_add.clicked.connect(self._add_row)
        self.btn_remove.clicked.connect(self._remove_row)

        title_row.addWidget(self.btn_add)
        title_row.addWidget(self.btn_remove)

        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.setSpacing(8)
        main_box.addLayout(title_row)

        self.driver_box = QVBoxLayout()
        self.driver_box.setSpacing(ConfigLayout.DRIVER_SPACING)
        main_box.addLayout(self.driver_box)

        self.driver_inputs = []
        self.drivers = []
        self.load_team()

    def load_team(self):
        """Load team and create driver input fields."""
        self.clear_drivers()
        team = get_team()
        if team:
            self.drivers = team.get('drivers', [])
            for driver in self.drivers:
                line_edit = QLineEdit(driver)
                line_edit.setFont(get_fonts(FONT.input_field))
                line_edit.setReadOnly(True)
                self.driver_box.addWidget(line_edit)
                self.driver_inputs.append(line_edit)

    def clear_drivers(self):
        """Remove all driver input widgets."""
        for line_edit in self.driver_inputs:
            self.driver_box.removeWidget(line_edit)
            line_edit.deleteLater()
        self.driver_inputs = []
        self.drivers = []

    def get_driver_inputs(self):
        """Return list of QLineEdit widgets for drivers."""
        return self.driver_inputs

    def get_driver_names(self):
        """Return list of driver names."""
        return self.drivers

    def _add_row(self):
        """Add a new driver input row (max 6)."""
        if len(self.driver_inputs) < 6:
            line_edit = QLineEdit()
            line_edit.setFont(get_fonts(FONT.input_field))
            self.driver_box.addWidget(line_edit)
            self.driver_inputs.append(line_edit)
        else:
            dialog = PopUp(
                title="Unable to add more rows",
                message="Maximum of 6 drivers allowed in a team.",
                buttons=["Ok"],
                type="warning",
                parent=self
            )
            dialog.exec()

    def _remove_row(self):
        """Remove the last driver input row, but always leave at least one."""
        if len(self.driver_inputs) > 1:
            line_edit = self.driver_inputs.pop()
            self.driver_box.removeWidget(line_edit)
            line_edit.deleteLater()
        else:
            dialog = PopUp(
                title="Can't remove more rows",
                message="You need at least one driver in a team.",
                buttons=["Ok"],
                type="warning",
                parent=self
            )
            dialog.exec()

    def _set_active(self, active):
        """Enable or disable the add/remove buttons."""
        self.btn_add.setEnabled(active)
        self.btn_remove.setEnabled(active)
