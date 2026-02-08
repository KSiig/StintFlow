"""
Window control buttons component.

Displays window control buttons (minimize, maximize, restore, close) with
the ability to handle window state changes. Designed to be placed at the
top of the right pane in the application.
"""

import sys
from pathlib import Path

from PyQt6.QtCore import QSize, Qt, QProcess
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QToolButton,
    QWidget,
    QApplication,
)

from core.utilities import resource_path
from core.errors import log, log_exception


# Window buttons configuration
BUTTON_SIZE = 28
BUTTON_ICON_SIZE = 16
BUTTON_SPACING = 4
BUTTON_CONTAINER_MARGIN_TOP = 8
BUTTON_CONTAINER_MARGIN_RIGHT = 0

# Window button icon paths
BUTTON_ICONS = {
    'minimize': 'resources/icons/window_buttons/minus.svg',
    'maximize': 'resources/icons/window_buttons/square.svg',
    'restore': 'resources/icons/window_buttons/restore.svg',
    'restart': 'resources/icons/window_buttons/restart.svg',
    'close': 'resources/icons/window_buttons/x.svg',
}


class WindowButtons(QWidget):
    """
    Window control buttons component.
    
    Displays minimize, maximize/restore, and close buttons with styling
    for the application window.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        
        self._create_layout()
    
    def _create_layout(self):
        """Create and configure the window buttons layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, BUTTON_CONTAINER_MARGIN_TOP, BUTTON_CONTAINER_MARGIN_RIGHT, 0)
        layout.setSpacing(BUTTON_SPACING)
        
        self.min_button = self._create_button(
            resource_path(BUTTON_ICONS['minimize']),
            self.window().showMinimized
        )

        self.max_button = self._create_button(
            resource_path(BUTTON_ICONS['maximize']),
            self.window().showMaximized
        )

        self.close_button = self._create_button(
            resource_path(BUTTON_ICONS['close']),
            self.window().close
        )

        self.restart_button = self._create_button(
            resource_path(BUTTON_ICONS['restart']),
            self._restart_app
        )
        self.restart_button.setToolTip('Restart')
        self.restart_button.setVisible(self._should_show_restart())

        self.normal_button = self._create_button(
            resource_path(BUTTON_ICONS['restore']),
            self.window().showNormal
        )
        self.normal_button.setVisible(False)

        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.restart_button,
            self.close_button,
        ]
        
        for button in buttons:
            layout.addWidget(button)
        
        layout.addStretch()
    
    def _create_button(self, icon_path, callback):
        """
        Create a styled window control button.
        
        Args:
            icon_path (str): Path to the icon SVG file
            callback (callable): Function to call when button is clicked
            
        Returns:
            QToolButton: The configured button
        """
        button = QToolButton(self)
        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE))
        button.clicked.connect(callback)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setFixedSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
        return button
    
    def window_state_changed(self, state):
        """
        Update button visibility based on window state.
        
        When window is maximized, hide the max button and show the normal button.
        
        Args:
            state (Qt.WindowState): The current window state
        """
        is_maximized = bool(state & Qt.WindowState.WindowMaximized)
        self.normal_button.setVisible(is_maximized)
        self.max_button.setVisible(not is_maximized)

    def _restart_app(self) -> None:
        """Restart the application using the current interpreter."""
        try:
            program, args = self._get_restart_command()
            started = QProcess.startDetached(program, args)

            if not started:
                log('ERROR', 'Failed to start restart process',
                    category='window_buttons', action='restart')
                return

            log('INFO', 'Restarting application',
                category='window_buttons', action='restart')
            QApplication.instance().quit()
            print()

        except Exception as exc:
            log_exception(exc, 'Failed to restart application',
                          category='window_buttons', action='restart')

    def _should_show_restart(self) -> bool:
        """Only show restart when running from a .py script."""
        script_path = Path(sys.argv[0]).resolve()
        return script_path.suffix.lower() == '.py'

    def _get_restart_command(self) -> tuple[str, list[str]]:
        """Build the restart command for script or bundled executable."""
        executable = sys.executable
        script_path = Path(sys.argv[0]).resolve()

        if script_path.suffix.lower() == '.py':
            return executable, [str(script_path), *sys.argv[1:]]

        return executable, list(sys.argv[1:])
