"""Compose the StrategiesView layout."""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QStackedWidget, QTabBar, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from ui.utilities.load_icon import load_icon
from ..SyncWidget import SyncWidget


def _setup_ui(self) -> None:
    """Set up tab bar, content frame, and action buttons."""
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setSpacing(12)

    tab_bar_frame = QFrame()
    tab_bar_frame.setObjectName("TabBarFrame")
    tab_bar_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    tab_bar_layout = QHBoxLayout(tab_bar_frame)
    tab_bar_layout.setContentsMargins(0, 0, 0, 0)
    tab_bar_layout.setSpacing(0)

    left_controls = QFrame()
    left_controls.setObjectName("StrategyHeaderControls")
    left_controls.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    left_controls_layout = QHBoxLayout(left_controls)
    left_controls_layout.setContentsMargins(0, 0, 0, 0)
    left_controls_layout.setSpacing(0)

    self.tab_bar = QTabBar()
    self.tab_bar.setObjectName("StrategyTabBar")
    self.tab_bar.currentChanged.connect(self._on_tab_changed)
    left_controls_layout.addWidget(self.tab_bar)

    add_btn = QPushButton()
    add_btn.setObjectName("AddStrategyButton")
    add_btn.setIcon(QIcon(load_icon("resources/icons/strategies/plus.svg", 16)))
    add_btn.setFixedSize(QSize(32, 32))
    add_btn.setToolTip("Create a new strategy")
    add_btn.clicked.connect(self._on_create_strategy)

    clone_btn = QPushButton()
    clone_btn.setObjectName("CloneStrategyButton")
    clone_btn.setIcon(QIcon(load_icon("resources/icons/strategies/copy-plus.svg", 16)))
    clone_btn.setFixedSize(QSize(32, 32))
    clone_btn.setToolTip("Clone selected strategy")
    clone_btn.clicked.connect(self._on_clone_strategy)

    left_controls_layout.addWidget(add_btn)
    left_controls_layout.addWidget(clone_btn)

    self.sync_widget = SyncWidget()
    self.sync_widget.sync_requested.connect(self._sync_current_strategy)

    tab_bar_layout.addWidget(left_controls)

    # move sync_widget out of the tab_bar_frame; place both controls in a
    # separate header_frame so the two areas are logically distinct.
    header_frame = QFrame()
    header_frame.setObjectName("HeaderFrame")
    header_layout = QHBoxLayout(header_frame)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(0)
    header_layout.addWidget(tab_bar_frame)
    header_layout.addStretch(1)
    header_layout.addWidget(self.sync_widget)

    content_frame = QFrame()
    content_frame.setObjectName("ContentFrame")
    content_layout = QVBoxLayout(content_frame)
    content_layout.setContentsMargins(0, 0, 0, 0)

    self.stacked_widget = QStackedWidget()
    self.stacked_widget.setObjectName("StrategyContent")
    content_layout.addWidget(self.stacked_widget)

    self.main_layout.addWidget(header_frame)
    self.main_layout.addWidget(content_frame)
