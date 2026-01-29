"""
Navigation menu for application sidebar.

Displays the application title/icon at the top, followed by navigation options
for different application features. Allows switching between different views
in the main workspace.

TODO: Integrate with models when available (navigation_model, selection_model)
TODO: Add stint tracking menu items when components are migrated
TODO: Add session picker when SessionPicker is migrated
"""

from typing import Callable

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.utilities import FONT, get_fonts, load_icon
from ui.models import ModelContainer
from core.utilities import resource_path
from core.errors import log, log_exception
from .stint_tracking import OverviewMainWindow, ConfigMainWindow
from .ClickableWidget import ClickableWidget


# Navigation menu configuration
MENU_WIDTH = 256
MENU_SPACING = 24
LOGO_SIZE = 24
MENU_ITEM_ICON_SIZE = 16
MENU_ITEM_ICON_COLOR = "#05fd7e"
TITLE_BOTTOM_MARGIN = 16

# Icon paths
ICON_LOGO = "resources/icons/logo.svg"
ICON_TIMER = "resources/icons/nav_menu/timer.svg"
ICON_EYE = "resources/icons/nav_menu/eye.svg"
ICON_COG = "resources/icons/nav_menu/cog.svg"
ICON_TARGET = "resources/icons/nav_menu/target.svg"


class NavigationMenu(QWidget):
    """
    Sidebar navigation menu for switching between application views.
    
    Displays the application title and icon at the top, followed by navigation
    options for different features and allows users to switch between views
    in the main workspace.
    """
    
    def __init__(self, parent: QWidget, models: ModelContainer = None) -> None:
        super().__init__(parent)
        self.models = models
        self._icon_cache: dict[tuple[str, int, str], QPixmap] = {}  # Cache for loaded icons (keyed by path, size, color)
        self._menu_items: dict[type, QWidget] = {}  # Track menu item widgets by their window class
        self._menu_item_icons: dict[QWidget, tuple[QLabel, str, int]] = {}  # Track (icon_label, icon_path, size) for each menu item
        self.__active_menu_item: QWidget | None = None  # Currently active menu item (private, use property)
        
        self._setup_styles()
        self._create_layout()
    
    @property
    def _active_menu_item(self) -> QWidget | None:
        """Get the currently active menu item."""
        return self.__active_menu_item
    
    @_active_menu_item.setter
    def _active_menu_item(self, value: QWidget | None) -> None:
        """Set the currently active menu item."""
        self.__active_menu_item = value
    
    def _setup_styles(self) -> None:
        """Load and apply navigation menu stylesheet."""
        try:
            with open(resource_path('resources/styles/navigation_menu.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'Navigation menu stylesheet not found', 
                         category='ui', action='load_stylesheet')
    
    def _create_layout(self) -> None:
        """Create and configure the navigation menu layout with all menu sections and items."""
        self.setFixedWidth(MENU_WIDTH)
        self.setObjectName("NavMenu")
        
        frame = QFrame()
        frame.setObjectName("NavMenu")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(frame)
        
        menu_layout = QVBoxLayout(frame)
        menu_layout.setSpacing(MENU_SPACING)
        menu_layout.setContentsMargins(8, 8, 8, 8)
        
        # Add title and icon at the top
        self._add_title_and_icon(menu_layout)
        
        # Stint tracking section
        stint_tracking_layout = self._create_menu_section("Stint tracking", ICON_TIMER)
        
        overview_item = self._create_menu_item(
            "Overview", 
            lambda: self._switch_to_overview(), 
            ICON_EYE
        )
        self._menu_items[OverviewMainWindow] = overview_item
        stint_tracking_layout.addWidget(overview_item)
        
        config_item = self._create_menu_item(
            "Config", 
            lambda: self._switch_to_config(), 
            ICON_COG
        )
        self._menu_items[ConfigMainWindow] = config_item
        stint_tracking_layout.addWidget(config_item)
        
        # TODO: Add Strategies menu item when component is migrated
        stint_tracking_layout.addWidget(self._create_menu_item("Strategies", lambda: print("Strategies clicked"), ICON_TARGET))
        menu_layout.addLayout(stint_tracking_layout)
        
        # Set overview as initially active
        self._set_active_menu_item(overview_item)
        
        menu_layout.addStretch()
        
        # TODO: Add session picker when SessionPicker is migrated
        # menu_layout.addWidget(self.session_picker)
    
    def _add_title_and_icon(self, layout: QVBoxLayout) -> None:
        """
        Add the application title and icon at the top of the menu.
        
        Loads and caches the logo icon, creates title label with appropriate font.
        
        Args:
            layout: The menu layout to add title/icon to
        """
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(MENU_SPACING, MENU_SPACING, 0, TITLE_BOTTOM_MARGIN)
        
        # Logo
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        logo.setPixmap(self._load_icon(ICON_LOGO, LOGO_SIZE))
        
        # Title
        title = QLabel("StintFlow")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setFont(get_fonts(FONT.title))
        
        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
    
    def _switch_to_overview(self) -> None:
        """Switch to the Overview window and update active menu item."""
        if self.models and self.models.navigation_model:
            overview_widget = self.models.navigation_model.widgets.get(OverviewMainWindow)
            if overview_widget:
                self.models.navigation_model.set_active_widget(overview_widget)
                self._set_active_menu_item(self._menu_items.get(OverviewMainWindow))
    
    def _switch_to_config(self) -> None:
        """Switch to the Config window and update active menu item."""
        if self.models and self.models.navigation_model:
            config_widget = self.models.navigation_model.widgets.get(ConfigMainWindow)
            if config_widget:
                self.models.navigation_model.set_active_widget(config_widget)
                self._set_active_menu_item(self._menu_items.get(ConfigMainWindow))
    
    def _update_menu_item_visual_state(self, menu_item: QWidget, is_active: bool) -> None:
        """
        Update menu item's visual state (property and style).
        
        Forces Qt to reapply stylesheets by unpolishing and polishing the widget tree.
        
        Args:
            menu_item: The menu item widget to update
            is_active: Whether the item should be styled as active
        """
        menu_item.setProperty("active", is_active)
        # Unpolish/polish the container and all its children to reapply styles
        for child in menu_item.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)
        menu_item.style().unpolish(menu_item)
        menu_item.style().polish(menu_item)
    
    def _update_menu_item_icon(self, menu_item: QWidget, is_active: bool) -> None:
        """
        Update menu item icon color based on active state.
        
        Active items use dark icon color, inactive items use accent color.
        
        Args:
            menu_item: The menu item widget to update icon for
            is_active: Whether the item is active (True = dark icon, False = accent icon)
        """
        if menu_item in self._menu_item_icons:
            icon_label, icon_path, size = self._menu_item_icons[menu_item]
            icon_color = "#04080B" if is_active else MENU_ITEM_ICON_COLOR
            icon_label.setPixmap(self._load_icon(icon_path, size, icon_color))
    
    def _set_active_menu_item(self, menu_item: QWidget = None) -> None:
        """
        Set the active menu item and update visual states.
        
        Updates both the previous and new active items' background colors and icon colors.
        Stores references to menu items for future icon color updates.
        
        Args:
            menu_item: The menu item widget to set as active
        """
        # Clear previous active item
        if self._active_menu_item:
            self._update_menu_item_visual_state(self._active_menu_item, False)
            self._update_menu_item_icon(self._active_menu_item, False)
        
        # Set new active item
        if menu_item:
            self._update_menu_item_visual_state(menu_item, True)
            self._update_menu_item_icon(menu_item, True)
            self._active_menu_item = menu_item
    
    def _load_icon(self, icon_path: str, size: int = MENU_ITEM_ICON_SIZE, 
                   color: str = MENU_ITEM_ICON_COLOR) -> QPixmap:
        """
        Load an icon with caching to avoid reloading the same icon multiple times.
        
        Icons are cached by (path, size, color) tuple. The cache persists for the
        lifetime of the NavigationMenu widget.
        
        Args:
            icon_path: Path to the icon file
            size: Size to scale the icon to (default: MENU_ITEM_ICON_SIZE)
            color: Hex color code to apply to the icon (default: MENU_ITEM_ICON_COLOR)
            
        Returns:
            The loaded and colorized icon, or a null pixmap if loading fails
        """
        # Create cache key from all parameters as tuple
        cache_key = (icon_path, size, color)
        
        # Return cached icon if available
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]
        
        # Load icon using utility function
        pixmap = load_icon(icon_path, size, color)
        
        # Cache the result
        self._icon_cache[cache_key] = pixmap
        
        return pixmap
    
    def _create_icon_label_layout(self, label_text: str, icon_path: str, 
                                   label_font, left_margin: int = MENU_SPACING, 
                                   object_name: str = None) -> tuple[QHBoxLayout, QLabel | None]:
        """
        Create horizontal layout with optional icon and label.
        
        Returns a tuple of (layout, icon_label) where icon_label may be None if no icon provided.
        
        Args:
            label_text: Text for the label
            icon_path: Path to SVG icon file (optional, can be None)
            label_font: Font to use for the label
            left_margin: Left margin/indentation in pixels (default: MENU_SPACING)
            object_name: Object name for the label (optional)
            
        Returns:
            Tuple of (layout, icon_label_widget) - icon_label_widget is None if no icon provided
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(left_margin, 8, 0, 8)
        layout.setSpacing(8)
        
        icon_label_widget = None
        
        # Icon (if provided)
        if icon_path:
            icon_label_widget = QLabel()
            icon_pixmap = self._load_icon(icon_path)
            icon_label_widget.setPixmap(icon_pixmap)
            icon_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label_widget)
        
        # Text label
        text_label = QLabel(label_text)
        if object_name:
            text_label.setObjectName(object_name)
        text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        text_label.setFont(label_font)
        
        layout.addWidget(text_label)
        layout.addStretch()
        
        return (layout, icon_label_widget)
    
    def _create_menu_section(self, label: str, icon_path: str = None) -> QVBoxLayout:
        """
        Create a menu section with a header label and optional icon.
        
        Returns a vertical layout ready to have menu items added to it.
        
        Args:
            label: Section header text
            icon_path: Path to SVG icon file (optional, can be None for text-only sections)
            
        Returns:
            Vertical layout for the menu section, configured with appropriate spacing
        """
        layout = QVBoxLayout()
        
        if icon_path:
            # Section with icon and label
            header_layout, _ = self._create_icon_label_layout(
                label, icon_path, get_fonts(FONT.menu_section), 
                MENU_SPACING, "NavMenuSectionLabel"
            )
            header_layout.setContentsMargins(MENU_SPACING, 0, 0, 4)
            layout.setSpacing(4)
            layout.addLayout(header_layout)
        else:
            # Simple text-only section
            section_label = QLabel(label)
            section_label.setObjectName("NavMenuSectionLabel")
            section_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            section_label.setFont(get_fonts(FONT.menu_section))
            section_label.setContentsMargins(0, 0, 0, 8)
            layout.setSpacing(8)
            layout.addWidget(section_label)
        
        return layout
    
    def _create_menu_item(self, label: str, callback: Callable, 
                         icon_path: str = None) -> QWidget:
        """
        Create a menu item with optional icon.
        
        Stores icon reference in _menu_item_icons for future color updates when active state changes.
        
        Args:
            label: Item label text
            callback: Function to call when item is clicked
            icon_path: Path to SVG icon file (optional, can be None for text-only items)
            
        Returns:
            Clickable menu item widget configured with appropriate styling
        """
        # Create clickable container
        container = ClickableWidget(callback)
        container.setObjectName("MenuItem")
        container.setProperty("active", False)
        
        if icon_path:
            # Create layout with icon and label
            layout, icon_label = self._create_icon_label_layout(
                label, icon_path, get_fonts(FONT.menu_section), MENU_SPACING * 2
            )
            container.setLayout(layout)
            # Store icon label reference for recoloring
            if icon_label:
                self._menu_item_icons[container] = (icon_label, icon_path, MENU_ITEM_ICON_SIZE)
        else:
            # Simple text-only item
            item = QLabel(label)
            item.setFont(get_fonts(FONT.menu_section))
            layout = QHBoxLayout()
            layout.setContentsMargins(MENU_SPACING * 2, 0, 0, 0)
            layout.addWidget(item)
            layout.addStretch()
            container.setLayout(layout)
        
        return container
