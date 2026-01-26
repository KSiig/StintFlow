"""
Custom title bar for frameless main window.

Provides window controls (minimize, maximize, close) and allows dragging
the window by the title bar area.
"""

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QStyle,
    QToolButton,
    QWidget,
)

from ui.utilities import FONT, get_fonts
from core.utilities import resource_path


class TitleBar(QWidget):
    """
    Custom title bar widget for frameless windows.
    
    Displays application title and icon, window control buttons, and handles
    window dragging via mouse movement on the title bar.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None

        title_bar_layout = self._create_layout()
        
        self._setup_title_and_icon(title_bar_layout)
        title_bar_layout.addStretch()
        self._setup_window_buttons(title_bar_layout)

    def _create_layout(self):
        """
        Create and configure the title bar layout.
        
        Returns:
            QHBoxLayout: The configured horizontal layout
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        return layout

    def _setup_title_and_icon(self, layout):
        """
        Create and add the favicon and title label to the layout.
        
        Args:
            layout (QHBoxLayout): The title bar layout to add widgets to
        """
        # Favicon
        self.favicon = QLabel()
        self.favicon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.favicon.setPixmap(QPixmap(resource_path("resources/favicons/favicon-32x32.png")))

        # Title
        self.title = QLabel("StintFlow")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setFont(get_fonts(FONT.title))

        layout.addWidget(self.favicon)
        layout.addWidget(self.title)

    def _setup_window_buttons(self, layout):
        """
        Create window control buttons and add them to the layout.
        
        Args:
            layout (QHBoxLayout): The title bar layout to add buttons to
        """
        self.min_button = self._create_button(
            QStyle.StandardPixmap.SP_TitleBarMinButton,
            self.window().showMinimized
        )

        self.max_button = self._create_button(
            QStyle.StandardPixmap.SP_TitleBarMaxButton,
            self.window().showMaximized
        )

        self.close_button = self._create_button(
            QStyle.StandardPixmap.SP_TitleBarCloseButton,
            self.window().close
        )

        self.normal_button = self._create_button(
            QStyle.StandardPixmap.SP_TitleBarNormalButton,
            self.window().showNormal
        )
        self.normal_button.setVisible(False)

        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        
        for button in buttons:
            layout.addWidget(button)

    def _create_button(self, icon_type, callback):
        """
        Create a styled window control button.
        
        Args:
            icon_type (QStyle.StandardPixmap): The standard icon type
            callback (callable): Function to call when button is clicked
            
        Returns:
            QToolButton: The configured button
        """
        button = QToolButton(self)
        icon = self.style().standardIcon(icon_type)
        button.setIcon(icon)
        button.clicked.connect(callback)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setFixedSize(QSize(28, 28))
        button.setStyleSheet("QToolButton { border: 0px; }")
        return button

    def window_state_changed(self, state):
        """
        Update button visibility based on window state.
        
        When window is maximized, hide the max button and show the normal button.
        
        Args:
            state (Qt.WindowState): The current window state
        """
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        """
        Record initial mouse position for window dragging.
        
        Args:
            event (QMouseEvent): The mouse press event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        """
        Move window based on mouse movement when dragging.
        
        Args:
            event (QMouseEvent): The mouse move event
        """
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        """
        Reset initial position tracking when mouse is released.
        
        Args:
            event (QMouseEvent): The mouse release event
        """
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
