"""Popup widget for selecting tire changes."""

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QPixmap

from core.utilities import resource_path
from ui.components.common import DropdownButton
from ui.utilities import load_icon


class TirePopup(QWidget):
    """Popup to pick tire compounds per wheel with quick-set buttons."""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        container = QFrame(self)
        container.setObjectName("TirePopupContainer")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(container)

        layout = QGridLayout(container)

        size_btn = QSize(36, 36)
        size_icon = QSize(24, 24)

        btn_x = QPushButton()
        btn_x.setIcon(QIcon(load_icon("resources/icons/tires/x.svg", size=size_icon.height() + 4, color="#D1D5DC")))
        btn_medium = QPushButton()
        medium_pixmap = QPixmap(resource_path("resources/icons/tires/medium.png"))
        btn_medium.setIcon(QIcon(medium_pixmap.scaledToHeight(size_icon.height(), Qt.TransformationMode.SmoothTransformation)))
        btn_wet = QPushButton()
        wet_pixmap = QPixmap(resource_path("resources/icons/tires/wet.png"))
        btn_wet.setIcon(QIcon(wet_pixmap.scaledToHeight(size_icon.height(), Qt.TransformationMode.SmoothTransformation)))

        btn_x.clicked.connect(lambda: self.set_all_tires(None))
        btn_medium.clicked.connect(lambda: self.set_all_tires("medium"))
        btn_wet.clicked.connect(lambda: self.set_all_tires("wet"))

        for btn in (btn_medium, btn_wet, btn_x):
            btn.setFixedSize(size_btn)
            btn.setIconSize(size_icon)
            btn.setObjectName("TirePopupQuickSetButton")
        btn_x.setIconSize(QSize(size_icon.width() + 3, size_icon.height() + 3))

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        btn_layout.addWidget(btn_x)
        btn_layout.addWidget(btn_medium)
        btn_layout.addWidget(btn_wet)
        btn_layout.addStretch()
        layout.addLayout(btn_layout, 0, 1)

        self.boxes = {}
        dropdown_items = [
            {"display": "", "value": "", "icon": None},
            {"display": "New", "value": "medium", "icon": resource_path("resources/icons/tires/medium.png")},
            {"display": "Used", "value": "used medium", "icon": resource_path("resources/icons/tires/medium.png")},
            {"display": "New", "value": "wet", "icon": resource_path("resources/icons/tires/wet.png")},
            {"display": "Used", "value": "used wet", "icon": resource_path("resources/icons/tires/wet.png")},
        ]
        for i, tire in enumerate(["FL", "FR", "RL", "RR"]):
            row = (i // 2) + 1
            col = (i % 2) * 2
            cb = DropdownButton(items=dropdown_items, current_value="", sort_items=False, parent=container, button_object_name="TirePopupDropdown")
            cb.valueChanged.connect(lambda _: self.dataChanged.emit())
            layout.addWidget(cb, row, col + 1)
            self.boxes[tire] = cb

    def set_values(self, data: dict) -> None:
        for tire in self.boxes:
            tire_changed = data["tires_changed"][tire.lower()]
            tire_compound = data[tire.lower()]["outgoing"]["compound"]
            if tire_changed:
                self.boxes[tire].set_value(tire_compound)
            else:
                self.boxes[tire].set_value("")

    def values(self) -> dict:
        return {k: v.get_value() for k, v in self.boxes.items()}

    def set_all_tires(self, compound: str | None = None) -> None:
        for tire in self.boxes:
            if compound:
                self.boxes[tire].set_value(compound)
            else:
                self.boxes[tire].set_value("")
            self.dataChanged.emit()
