"""
Main application window.

Orchestrates the overall UI layout including title bar, navigation menu,
and content workspace. Manages window state and content switching.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedLayout,
    QWidget,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QEvent

from .TitleBar import TitleBar


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Sets up the overall application layout with title bar, navigation menu,
    and scrollable content area. Manages switching between different views.
    """
    
    def __init__(self):
        super().__init__()
        
        self._setup_window_properties()
        self.title_bar = self._create_title_bar()
        self.work_space_layout = self._create_workspace_layout()
        self.central_scroll_area = self._create_scroll_area()
        self.central_container = self._create_central_container()
        
        self._setup_layouts()

    def _setup_window_properties(self):
        """Configure basic window properties (size, flags, style)."""
        self.setGeometry(200, 100, 1400, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def _create_title_bar(self):
        """
        Create and return the title bar widget.
        
        Returns:
            TitleBar: The configured title bar instance
        """
        return TitleBar(self)

    def _create_workspace_layout(self):
        """
        Create the main workspace layout.
        
        Returns:
            QHBoxLayout: The workspace layout
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(11, 11, 11, 11)
        return layout

    def _create_scroll_area(self):
        """
        Create the scrollable content area.
        
        Returns:
            QScrollArea: The configured scroll area
        """
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        return scroll_area

    def _create_central_container(self):
        """
        Create the central container with stacked layout for view switching.
        
        Returns:
            QWidget: Container widget with stacked layout
        """
        container = QWidget()
        layout = QStackedLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.central_scroll_area.setWidget(container)
        self.central_container_layout = layout
        
        return container

    def _setup_layouts(self):
        """Assemble all layout components into the main window."""
        # TODO: Uncomment navigation menu when implemented
        # nav_menu = NavigationMenu(self, {...})
        # self.work_space_layout.addWidget(nav_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.work_space_layout.addWidget(self.central_scroll_area)

        # Create main widget layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(self.work_space_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _change_workspace_widget(self):
        """
        Switch the active workspace widget.
        
        Called when the navigation model's active widget changes.
        Ensures the new widget is added to the layout and displayed.
        
        TODO: Implement when models are migrated.
        """
        pass

    def changeEvent(self, event):
        """
        Handle window state changes.
        
        Updates the title bar when window state changes (minimize, maximize, etc.).
        """
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()
