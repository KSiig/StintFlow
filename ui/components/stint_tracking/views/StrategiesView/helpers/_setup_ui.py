"""Compose the StrategiesView layout."""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QStackedWidget, QTabBar, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from ui.utilities.load_icon import load_icon


def _setup_ui(self) -> None:
    """Set up tab bar, content frame, and action buttons."""
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setSpacing(12)

    tab_bar_frame = QFrame()
    tab_bar_frame.setObjectName("TabBarFrame")
    tab_bar_frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    tab_bar_layout = QHBoxLayout(tab_bar_frame)
    tab_bar_layout.setContentsMargins(0, 0, 0, 0)
    tab_bar_layout.setSpacing(0)

    self.tab_bar = QTabBar()
    self.tab_bar.setObjectName("StrategyTabBar")
    self.tab_bar.currentChanged.connect(self._on_tab_changed)
    tab_bar_layout.addWidget(self.tab_bar)

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

    tab_bar_layout.addWidget(add_btn)
    tab_bar_layout.addWidget(clone_btn)

    content_frame = QFrame()
    content_frame.setObjectName("ContentFrame")
    content_layout = QVBoxLayout(content_frame)
    content_layout.setContentsMargins(0, 0, 0, 0)

    self.stacked_widget = QStackedWidget()
    self.stacked_widget.setObjectName("StrategyContent")
    content_layout.addWidget(self.stacked_widget)

    self.main_layout.addWidget(tab_bar_frame)
    self.main_layout.addWidget(content_frame)
