"""
Navigation menu for application sidebar.

Displays the application title/icon at the top, followed by navigation options
for different application features. Allows switching between different views
in the main workspace.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.utilities import FONT, get_fonts, get_cached_icon
from ui.models import ModelContainer
from core.utilities import resource_path
from core.errors import log_exception
from ..stint_tracking import OverviewView, ConfigView, StrategiesView
from ..settings import SettingsView
from .SessionPicker import SessionPicker
from .menu_item_factory import MenuItemConfig, create_menu_item, update_menu_item_state
from .constants import (
    MENU_WIDTH,
    MENU_SPACING,
    LOGO_SIZE,
    TITLE_BOTTOM_MARGIN,
    MENU_SECTION_ICON_COLOR,
    ICON_LOGO,
    ICON_TIMER,
    ICON_EYE,
    ICON_COG,
    ICON_TARGET,
    ICON_SETTINGS
)


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
        self._menu_items: dict[type, MenuItemConfig] = {}  # Track menu items by window class
        self._active_menu_item: MenuItemConfig = None  # Currently active menu item
        
        self._setup_styles()
        self._create_layout()

        self.models.selection_model.eventChanged.connect(self._update_event_selection)
        self.models.selection_model.sessionChanged.connect(self._update_event_selection)
    
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
        menu_layout.setContentsMargins(0, 8, 0, 0)
        
        # Add title and icon at the top
        self._add_title_and_icon(menu_layout)
        
        # Stint tracking section
        stint_tracking_layout = self._create_menu_section("Stint tracking", ICON_TIMER)
        
        # Create menu items
        overview_item = create_menu_item("Overview", lambda: self._switch_to_overview(), ICON_EYE)
        overview_item.window_class = OverviewView
        self._menu_items[OverviewView] = overview_item
        stint_tracking_layout.addWidget(overview_item.widget)
        
        config_item = create_menu_item("Config", lambda: self._switch_to_config(), ICON_COG)
        config_item.window_class = ConfigView
        self._menu_items[ConfigView] = config_item
        stint_tracking_layout.addWidget(config_item.widget)
        
        strategies_item = create_menu_item("Strategies", lambda: self._switch_to_strategies(), ICON_TARGET)
        strategies_item.window_class = StrategiesView
        self._menu_items[StrategiesView] = strategies_item
        stint_tracking_layout.addWidget(strategies_item.widget)
        
        menu_layout.addLayout(stint_tracking_layout)
        
        # Set overview as initially active
        self._set_active_menu_item(overview_item)
        
        menu_layout.addStretch()

        # Settings item (bottom)
        settings_item = create_menu_item("Settings", lambda: self._switch_to_settings(), ICON_SETTINGS, menu_spacing=32)
        settings_item.window_class = SettingsView
        settings_item.widget.setObjectName("MenuItemSettings")
        self._menu_items[SettingsView] = settings_item
        menu_layout.addWidget(settings_item.widget)
        
        # Add session picker at the bottom
        self.session_picker = SessionPicker(models=self.models)
        menu_layout.addWidget(self.session_picker)

    def _update_event_selection(self):
        self.session_picker.reload()
    
    def _add_title_and_icon(self, layout: QVBoxLayout) -> None:
        """
        Add the application title and icon at the top of the menu.
        
        Args:
            layout: The menu layout to add title/icon to
        """
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(MENU_SPACING, MENU_SPACING, 0, TITLE_BOTTOM_MARGIN)
        
        # Logo
        logo = QLabel()
        logo.setObjectName("TitleLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        logo.setPixmap(get_cached_icon(ICON_LOGO, LOGO_SIZE, MENU_SECTION_ICON_COLOR))
        
        # Title
        title = QLabel("StintFlow")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setFont(get_fonts(FONT.title))
        
        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
    
    def _switch_to_overview(self) -> None:
        """Switch to the Overview window and update active menu item."""
        if self.models and self.models.navigation_model:
            overview_widget = self.models.navigation_model.widgets.get(OverviewView)
            if overview_widget:
                self.models.navigation_model.set_active_widget(overview_widget)
                item_config = self._menu_items.get(OverviewView)
                if item_config:
                    self._set_active_menu_item(item_config)
    
    def _switch_to_config(self) -> None:
        """Switch to the Config window and update active menu item."""
        if self.models and self.models.navigation_model:
            config_widget = self.models.navigation_model.widgets.get(ConfigView)
            if config_widget:
                self.models.navigation_model.set_active_widget(config_widget)
                item_config = self._menu_items.get(ConfigView)
                if item_config:
                    self._set_active_menu_item(item_config)
    
    def _switch_to_strategies(self) -> None:
        """Switch to the Strategies window and update active menu item."""
        if self.models and self.models.navigation_model:
            strategies_widget = self.models.navigation_model.widgets.get(StrategiesView)
            if strategies_widget:
                self.models.navigation_model.set_active_widget(strategies_widget)
                item_config = self._menu_items.get(StrategiesView)
                if item_config:
                    self._set_active_menu_item(item_config)

    def _switch_to_settings(self) -> None:
        """Switch to the Settings window and update active menu item."""
        if self.models and self.models.navigation_model:
            settings_widget = self.models.navigation_model.widgets.get(SettingsView)
            if settings_widget:
                self.models.navigation_model.set_active_widget(settings_widget)
                item_config = self._menu_items.get(SettingsView)
                if item_config:
                    self._set_active_menu_item(item_config)
    
    def _set_active_menu_item(self, item_config: MenuItemConfig = None) -> None:
        """
        Set the active menu item and update visual states.
        
        Updates both the previous and new active items' background colors and icon colors.
        
        Args:
            item_config: The menu item configuration to set as active (None to clear)
        """
        # Validate that item_config is a registered menu item
        if item_config and item_config not in self._menu_items.values():
            return
        
        # Clear previous active item
        if self._active_menu_item:
            update_menu_item_state(self._active_menu_item, False)
        
        # Set new active item
        if item_config:
            update_menu_item_state(item_config, True)
            self._active_menu_item = item_config
    
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
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(MENU_SPACING, 0, 0, 4)
            header_layout.setSpacing(8)
            
            # Icon
            icon_label = QLabel()
            icon_label.setObjectName("NavMenuSectionIcon")
            icon_pixmap = get_cached_icon(icon_path, LOGO_SIZE, MENU_SECTION_ICON_COLOR)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(icon_label)
            
            # Text label
            text_label = QLabel(label)
            text_label.setObjectName("NavMenuSectionLabel")
            text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            text_label.setFont(get_fonts(FONT.menu_section))
            header_layout.addWidget(text_label)
            header_layout.addStretch()
            
            layout.setSpacing(4)
            layout.addLayout(header_layout)
        else:
            # Simple text-only section
            section_label = QLabel(label)
            section_label.setObjectName("NavMenuSectionLabel")
            section_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            section_label.setFont(get_fonts(FONT.menu_section))
            section_label.setContentsMargins(MENU_SPACING, 0, 0, 8)
            layout.setSpacing(8)
            layout.addWidget(section_label)
        
        return layout
