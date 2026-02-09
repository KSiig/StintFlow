"""
Reusable dropdown button widget with custom popup.

A button that opens a popup menu with selectable items,
styled consistently and easy to use throughout the application.
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics

from core.utilities import resource_path
from core.errors import log, log_exception


class DropdownButton(QWidget):
    """
    Custom dropdown button with popup selection menu.
    
    Creates a button that displays the current value and opens a popup
    with selectable items when clicked. Fully customizable and reusable.
    """
    
    valueChanged = pyqtSignal(str)
    
    def __init__(
        self,
        items: list[str],
        current_value: str = "",
        button_object_name: str = "DropdownButton",
        popup_object_name: str = "DropdownPopup",
        item_object_name: str = "DropdownPopupItem",
        load_styles: bool = True,
        parent=None
    ):
        """
        Initialize dropdown button.
        
        Args:
            items: List of selectable items
            current_value: Initial value to display
            button_object_name: QSS object name for the button
            popup_object_name: QSS object name for the popup container
            item_object_name: QSS object name for popup items
            parent: Parent widget
        """
        super().__init__(parent)
        
        if load_styles:
            self._setup_styles()
        self.items = items
        self.button_object_name = button_object_name
        self.popup_object_name = popup_object_name
        self.item_object_name = item_object_name
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create button
        self.btn = QPushButton(current_value)
        self.btn.setObjectName(button_object_name)
        self.btn.clicked.connect(self._show_popup)
        layout.addWidget(self.btn)
        
        # Create popup (will be shown on demand)
        self.popup = DropdownPopup(
            items=items,
            popup_object_name=popup_object_name,
            item_object_name=item_object_name,
            parent=self
        )
        self.popup.valueChanged.connect(self._on_value_changed)

    def _setup_styles(self) -> None:
        """Load and apply dropdown stylesheet."""
        try:
            with open(resource_path('resources/styles/dropdown.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Dropdown stylesheet not found', 
                category='dropdown', action='load_stylesheet')
        except Exception as e:
            log_exception('Error loading dropdown stylesheet', e,
                          category='dropdown', action='load_stylesheet')
    
    def _show_popup(self):
        """Show popup below the button."""
        # Position popup below the button
        pos = self.btn.mapToGlobal(self.btn.rect().bottomLeft())
        self.popup.move(pos.x(), pos.y() + 8)
        self.popup.show()
    
    def _on_value_changed(self, value: str):
        """Handle value change from popup."""
        self.btn.setText(value)
        self.valueChanged.emit(value)
    
    def set_value(self, value: str):
        """Set the current value displayed on the button."""
        self.btn.setText(value)

    def set_text_alignment_left(self, padding_left: int = 0) -> None:
        """Left-align the text inside the button with optional padding."""
        if padding_left > 0:
            self.btn.setStyleSheet(
                f"text-align: left; padding-left: {padding_left}px;"
            )
            return

        self.btn.setStyleSheet("text-align: left;")

    def set_items(self, items: list[str]) -> None:
        """Replace popup items and keep current value when possible."""
        self.items = items
        current_value = self.btn.text()
        self.popup.setParent(None)
        self.popup.deleteLater()
        self.popup = DropdownPopup(
            items=items,
            popup_object_name=self.popup_object_name,
            item_object_name=self.item_object_name,
            parent=self
        )
        self.popup.valueChanged.connect(self._on_value_changed)

        if current_value in items:
            self.btn.setText(current_value)
        elif items:
            self.btn.setText(items[0])
        else:
            self.btn.setText("")
    
    def get_value(self) -> str:
        """Get the current value displayed on the button."""
        return self.btn.text()


class DropdownPopup(QWidget):
    """
    Popup widget for dropdown selection.
    
    Shows a list of buttons for selecting values.
    """
    
    valueChanged = pyqtSignal(str)
    
    def __init__(
        self,
        items: list[str],
        popup_object_name: str = "DropdownPopup",
        item_object_name: str = "DropdownPopupItem",
        parent=None
    ):
        """
        Initialize dropdown popup.
        
        Args:
            items: List of selectable items
            popup_object_name: QSS object name for the popup container
            item_object_name: QSS object name for popup items
            parent: Parent widget
        """
        super().__init__(parent, Qt.WindowType.Popup)
        self.setObjectName(f"{popup_object_name}Container")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)
        
        # Create main layout for the popup
        popup_layout = QVBoxLayout(self)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.setSpacing(0)
        
        # Create frame to wrap the buttons (allows styling the border)
        frame = QFrame(self)
        frame.setObjectName(popup_object_name)
        popup_layout.addWidget(frame)
        
        # Create layout inside the frame
        layout = QVBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.buttons = []
        max_text_width = 0
        
        # Create buttons for each item
        for item in items:
            btn = QPushButton(item if item else "(None)")
            btn.setObjectName(item_object_name)
            btn.setStyleSheet("text-align: left;")
            btn.clicked.connect(lambda checked, value=item: self._select_value(value))
            layout.addWidget(btn)
            self.buttons.append(btn)
            
            # Track widest text
            metrics = QFontMetrics(btn.font())
            text_width = metrics.boundingRect(btn.text()).width()
            if text_width > max_text_width:
                max_text_width = text_width
        
        # Set popup width to accommodate widest text + padding
        self.setFixedWidth(max_text_width + 40)
    
    def _select_value(self, value: str):
        """Handle value selection."""
        self.valueChanged.emit(value)
        self.hide()
