"""Create and configure the session picker layout."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy

from ._add_combo_icon import _add_combo_icon
from ._create_combo_box import _create_combo_box
from ...constants import (
    FRAME_BOTTOM_MARGIN,
    FRAME_LEFT_MARGIN,
    FRAME_RIGHT_MARGIN,
    FRAME_TOP_MARGIN,
    COMBO_SPACING,
    ICON_CALENDAR,
    ICON_CLOCK,
)


def _create_layout(self) -> None:
    """Create the session picker layout with two combo boxes."""
    frame = QFrame()
    frame.setObjectName("ComboBoxes")
    frame.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    frame.setContentsMargins(0, FRAME_TOP_MARGIN, 0, FRAME_BOTTOM_MARGIN)

    root_widget_layout = QVBoxLayout(self)
    root_widget_layout.setContentsMargins(0, 0, 0, 0)
    root_widget_layout.addWidget(frame)

    root_layout = QVBoxLayout(frame)
    root_layout.setContentsMargins(FRAME_LEFT_MARGIN, 0, FRAME_RIGHT_MARGIN, 0)
    root_layout.setSpacing(COMBO_SPACING)
    root_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.events = _create_combo_box(self)
    self.sessions = _create_combo_box(self)

    self.events.currentIndexChanged.connect(self._on_event_changed)
    self.sessions.currentIndexChanged.connect(self._on_session_changed)

    _add_combo_icon(self, self.events, ICON_CALENDAR)
    _add_combo_icon(self, self.sessions, ICON_CLOCK)

    root_layout.addWidget(self.events)
    root_layout.addWidget(self.sessions)
