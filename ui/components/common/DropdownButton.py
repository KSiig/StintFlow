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

    By default the entries are **sorted alphabetically** by their display
    string; pass ``sort_items=False`` to preserve the order provided by the
    caller.  The ``set_sorting`` helper can toggle this behaviour at runtime.
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
        sort_items: bool = True,
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

        # keep the original list around so we can re-sort if the user toggles
        # the sorting behaviour later.
        self._raw_items = items
        self.sort_items = sort_items

        # construct normalized items and mappings
        self.items = self._normalize_items(items)
        if self.sort_items:
            self.items.sort(key=lambda d: d['display'].lower())

        # mappings for quick lookup by value
        self.value_to_display = {d['value']: d['display'] for d in self.items}
        self.value_to_icon = {d['value']: d['icon'] for d in self.items}

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

    def _normalize_items(self, items: list) -> list[dict]:
        """Convert raw item descriptions into normalized dicts.

        Accepts the same flexible formats documented in ``__init__`` and
        ``set_items``.  Returns a list of ``{'display', 'value', 'icon'}``
        dictionaries.  The caller may sort the returned list as needed.
        """
        normalized = []
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
                    # second element could be icon path or actual value
                    second = it[1]
                    if isinstance(second, (str, QIcon)) and (
                        (isinstance(second, str) and (second.endswith('.png') or second.endswith('.svg')))
                    ):
                        display = str(it[0])
                        value = display
                        icon = second
                    else:
                        display = str(it[0])
                        value = second
                else:
                    display = str(it[0])
                    value = it[1]
                    icon = it[2]
            else:
                display = str(it)
                value = display
            if isinstance(icon, str):
                icon = QIcon(icon)
            if value is None:
                value = display
            normalized.append({'display': display, 'value': value, 'icon': icon})
        return normalized

    def set_sorting(self, enabled: bool) -> None:
        """Enable or disable alphabetical sorting of entries.

        When toggled the list is immediately rebuilt from the original raw
        items passed to the widget.  This keeps the ``value``/``display``
        mappings in sync.
        """
        self.sort_items = enabled
        # rebuild the list using the preserved raw sequence
        self.set_items(self._raw_items)
    
    def _show_popup(self):
        """Show popup above the button.

        The original implementation placed the dropdown immediately below the
        button. For certain layouts (e.g. when the button is near the bottom of
        the window) it's preferable to open the menu upwards. We calculate the
        global top-left point of the button, show the popup to initialize its
        geometry, then reposition it so its bottom edge sits a small gap above
        the button.
        """
        # Determine global position of the button's top left
        pos = self.btn.mapToGlobal(self.btn.rect().topLeft())

        # Show first so that height() reflects the real size (sizeHint may not be
        # accurate if the widget hasn't been laid out yet).
        self.popup.show()

        # Move the popup so that it sits above the button with an 8px gap
        popup_height = self.popup.height()
        self.popup.move(pos.x(), pos.y() - popup_height - 8)

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
        self._raw_items = items

        # normalize and optionally sort
        self.items = self._normalize_items(items)
        if self.sort_items:
            self.items.sort(key=lambda d: d['display'].lower())

        # rebuild lookup maps
        self.value_to_display = {d['value']: d['display'] for d in self.items}
        self.value_to_icon = {d['value']: d['icon'] for d in self.items}

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
