from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget


def create_main_layout(navigation_menu: QWidget, right_pane: QWidget) -> QFrame:
    """Assemble the main two-pane layout for the application window."""
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_layout.addWidget(navigation_menu, alignment=Qt.AlignmentFlag.AlignLeft)
    main_layout.addWidget(right_pane)

    border_frame = QFrame()
    border_frame.setObjectName("BorderFrame")
    border_frame.setLayout(main_layout)
    border_frame.setFrameShape(QFrame.Shape.NoFrame)
    return border_frame
