"""
Reusable dropdown button widget with custom popup.

A button that opens a popup menu with selectable items,
styled consistently and easy to use throughout the application.
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QIcon

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
        # Normalize items into list of dicts containing display text, internal value and optional icon.
        # Supported item formats:
        #   * simple string -> display==value==string, no icon
        #   * tuple 2-tuple -> (display, value) or (display, icon) if second is a path/object
        #   * tuple 3-tuple -> (display, value, icon)
        #   * dict -> { 'display': str, 'value': str, 'icon': str|QIcon }
        SELF_GAP = 8
        self.items = []
        # mappings for quick lookup by value
        self.value_to_display = {}
        self.value_to_icon = {}
        for it in items:
            display = ''
            value = None
            icon = None
            if isinstance(it, dict):
                display = it.get('display') or it.get('text', '')
                value = it.get('value', display)
                icon = it.get('icon')
            elif isinstance(it, tuple):
                if len(it) == 1:
                    display = str(it[0])
                    value = display
                elif len(it) == 2:
                    # ambiguous: second element may be value or icon
                    if isinstance(it[1], (str, QIcon)) and (it[1].endswith('.png') or it[1].endswith('.svg') if isinstance(it[1], str) else False):
                        display = str(it[0])
                        value = display
                        icon = it[1]
                    else:
                        display = str(it[0])
                        value = it[1]
                else:
                    display = str(it[0])
                    value = it[1]
                    icon = it[2]
            else:
                display = str(it)
                value = display
            if isinstance(icon, str):
                icon = QIcon(icon)
                # no modification to icon; spacing will be added when updating button text
            pass

            if value is None:
                value = display

            self.items.append({'display': display, 'value': value, 'icon': icon})
            self.value_to_display[value] = display
            self.value_to_icon[value] = icon

        self.button_object_name = button_object_name
        self.popup_object_name = popup_object_name
        self.item_object_name = item_object_name

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create button
        self.btn = QPushButton("")
        self.btn.setObjectName(button_object_name)
        self.btn.clicked.connect(self._show_popup)
        layout.addWidget(self.btn)

        # track internal value separately from button text
        self.current_value = None

        # apply initial value (this will also set display/icon)
        if current_value is not None:
            self.set_value(current_value)

        # Create popup (will be shown on demand)
        self.popup = DropdownPopup(
            items=self.items,
            popup_object_name=popup_object_name,
            item_object_name=item_object_name,
            parent=self
        )
        self.popup.valueChanged.connect(self._on_value_changed)

    # icon padding no longer required; spacing handled by text prefix
    # def _pad_icon(self, icon, gap: int = 8):
    #     return icon

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

    def _pad_text(self, text: str, gap: int = 1) -> str:
        """Return text prefixed with enough spaces to create `gap` pixels.

        This avoids touching the icon itself. We use the button's font metrics
        so the spacing matches what the user will see in the UI.
        """
        if not text:
            return text
        fm = QFontMetrics(self.btn.font())
        space_width = fm.boundingRect(' ').width() or 1
        count = (gap + space_width - 1) // space_width  # ceil
        return ' ' * count + text
    
    def _on_value_changed(self, value: str):
        """Handle value change from popup.

        Stores the internal value and updates button display accordingly.
        """
        # save internal value
        self.current_value = value
        disp = self.value_to_display.get(value, value)
        self.btn.setText(self._pad_text(disp))
        ico = self.value_to_icon.get(value)
        if ico:
            self.btn.setIcon(ico)
        else:
            self.btn.setIcon(QIcon())
        self.valueChanged.emit(value)
    
    def set_value(self, value: str):
        """Set the current internal value and update display/icon.

        Arg:
            value: internal value (may also be a display string; will convert if needed)
        """
        # if passed a display string, convert to value
        if value in self.value_to_display.values():
            # reverse lookup
            for val, disp in self.value_to_display.items():
                if disp == value:
                    value = val
                    break
        self.current_value = value
        disp = self.value_to_display.get(value, value)
        self.btn.setText(self._pad_text(disp))
        ico = self.value_to_icon.get(value)
        if ico:
            self.btn.setIcon(ico)
        else:
            self.btn.setIcon(QIcon())

    def set_text_alignment_left(self, padding_left: int = 0) -> None:
        """Left-align the text inside the button with optional padding."""
        if padding_left > 0:
            self.btn.setStyleSheet(
                f"text-align: left; padding-left: {padding_left}px;"
            )
            return

        self.btn.setStyleSheet("text-align: left;")

    def set_items(self, items: list[str]) -> None:
        """Replace popup items and keep current value when possible.

        Supports same flexible item formats as constructor.
        """
        # rebuild normalization (value/display/icon) with icon padding
        SELF_GAP = 8
        self.items = []
        self.value_to_display = {}
        self.value_to_icon = {}
        for it in items:
            display = ''
            value = None
            icon = None
            if isinstance(it, dict):
                display = it.get('display') or it.get('text', '')
                value = it.get('value', display)
                icon = it.get('icon')
            elif isinstance(it, tuple):
                if len(it) == 1:
                    display = str(it[0]); value = display; icon = None
                elif len(it) == 2:
                    if isinstance(it[1], str) and (it[1].endswith('.png') or it[1].endswith('.svg')):
                        display = str(it[0]); value = display; icon = it[1]
                    else:
                        display = str(it[0]); value = it[1]; icon = None
                else:
                    display = str(it[0]); value = it[1]; icon = it[2]
            else:
                display = str(it); value = display; icon = None
            if isinstance(icon, str):
                icon = QIcon(icon)
            # pad icon if present
            if icon and not icon.isNull():
                icon = self._pad_icon(icon, SELF_GAP)
            if value is None:
                value = display
            self.items.append({'display': display, 'value': value, 'icon': icon})
            self.value_to_display[value] = display
            self.value_to_icon[value] = icon

        current_value = self.btn.text()
        self.popup.setParent(None)
        self.popup.deleteLater()
        self.popup = DropdownPopup(
            items=self.items,
            popup_object_name=self.popup_object_name,
            item_object_name=self.item_object_name,
            parent=self
        )
        self.popup.valueChanged.connect(self._on_value_changed)

        if current_value in self.value_to_display:
            disp = self.value_to_display.get(current_value)
            self.btn.setText(self._pad_text(disp))
            ico = self.value_to_icon.get(current_value)
            if ico:
                self.btn.setIcon(ico)
        elif self.items:
            first_val = self.items[0]['value']
            self.btn.setText(self._pad_text(self.items[0]['display']))
            ico = self.items[0].get('icon')
            if ico:
                self.btn.setIcon(ico)
        else:
            self.btn.setText("")
            self.btn.setIcon(QIcon())
    
    def get_value(self) -> str:
        """Get the current internal value (not the display text)."""
        return self.current_value


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
        for entry in items:
            # entry may already be normalized dict from outer class
            if isinstance(entry, dict):
                display = entry.get('display', '')
                value = entry.get('value', display)
                icon = entry.get('icon')
            elif isinstance(entry, tuple):
                if len(entry) == 1:
                    display = str(entry[0]); value = display; icon = None
                elif len(entry) == 2:
                    # heuristic: if second element looks like icon path use as icon
                    if isinstance(entry[1], str) and (entry[1].endswith('.png') or entry[1].endswith('.svg')):
                        display = str(entry[0]); value = display; icon = entry[1]
                    else:
                        display = str(entry[0]); value = entry[1]; icon = None
                else:
                    display = str(entry[0]); value = entry[1]; icon = entry[2]
            else:
                display = str(entry); value = display; icon = None

            # pad display text using parent method if available
            text_to_show = display if display else "(None)"
            parent = self.parent()
            if parent and hasattr(parent, '_pad_text'):
                try:
                    text_to_show = parent._pad_text(text_to_show)
                except Exception:
                    pass

            btn = QPushButton(text_to_show)
            btn.setObjectName(item_object_name)
            btn.setStyleSheet("text-align: left;")
            if icon:
                if isinstance(icon, str):
                    btn.setIcon(QIcon(icon))
                else:
                    btn.setIcon(icon)
            btn.clicked.connect(lambda checked, val=value: self._select_value(val))
            layout.addWidget(btn)
            self.buttons.append(btn)
            
            # Track widest text (icon not included in width calc)
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
