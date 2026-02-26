"""
Strategies view for managing race strategies.

Displays tabbed interface with main strategy creator and existing strategies.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabBar, QStackedWidget, QFrame, QPushButton, QSizePolicy, QApplication
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from bson import ObjectId
from core.errors import log, log_exception
from core.utilities import resource_path
from core.database import create_strategy, get_strategies
from ui.models import ModelContainer
from ui.models.stint_helpers import sanitize_stints
from ui.utilities import load_icon
from ..strategies import StrategyTab


class StrategiesView(QWidget):
    """
    Main view for race strategy management.
    
    Displays a tabbed interface where:
    - First tab is the strategy creator (MainTab)
    - Subsequent tabs show existing strategies with editable stint tables
    """
    
    strategy_created = pyqtSignal(dict)  # Emitted when new strategy is created
    
    def __init__(self, models: ModelContainer):
        """
        Initialize strategies view.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.models = models
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        
        # Connect to session changes to reload strategies
        self.selection_model.sessionChanged.connect(self._on_session_changed)
        
        self._setup_ui()
        self._setup_styles()
        self._load_strategies()

    def _setup_styles(self) -> None:
        """Load and apply navigation menu stylesheet."""
        try:
            with open(resource_path('resources/styles/strategies.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'Navigation menu stylesheet not found', 
                         category='ui', action='load_stylesheet')
    
    def _setup_ui(self):
        """Set up the main layout with separated tab bar and content area."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(12)  # Space between tab bar and content
        self.setLayout(self.main_layout)
        
        # Tab bar container (for rounded corners styling)
        tab_bar_frame = QFrame()
        tab_bar_frame.setObjectName("TabBarFrame")
        # limit width to its contents so the button stays next to the tabs
        tab_bar_frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        tab_bar_layout = QHBoxLayout(tab_bar_frame)  # Horizontal to add button
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)
        tab_bar_layout.setSpacing(0)
        
        # Tab bar
        self.tab_bar = QTabBar()
        self.tab_bar.setObjectName("StrategyTabBar")
        # only use as much horizontal space as required by the tabs
        self.tab_bar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        tab_bar_layout.addWidget(self.tab_bar)
        
        # no stretch – frame width is minimal so button appears directly after tabs
        # tab_bar_layout.addStretch()
        
        # Add strategy button
        add_btn = QPushButton()
        add_btn.setObjectName("AddStrategyButton")
        add_btn.setIcon(QIcon(load_icon('resources/icons/strategies/plus.svg', 16)))
        add_btn.setFixedSize(32, 32)
        add_btn.setToolTip("Create a new strategy")
        add_btn.clicked.connect(self._on_create_strategy)

        # Clone strategy button
        clone_btn = QPushButton()
        clone_btn.setObjectName("CloneStrategyButton")
        clone_btn.setIcon(QIcon(load_icon('resources/icons/strategies/copy-plus.svg', 16)))
        clone_btn.setFixedSize(32, 32)
        clone_btn.setToolTip("Clone selected strategy")

        tab_bar_layout.addWidget(add_btn)
        tab_bar_layout.addWidget(clone_btn)
        
        # Content area container (for rounded corners styling)
        content_frame = QFrame()
        content_frame.setObjectName("ContentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for tab content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("StrategyContent")
        content_layout.addWidget(self.stacked_widget)
        
        # Add to main layout
        self.main_layout.addWidget(tab_bar_frame)
        self.main_layout.addWidget(content_frame)
    
    def _on_tab_changed(self, index: int):
        """Handle tab change by switching stacked widget page."""
        self.stacked_widget.setCurrentIndex(index)
    
    def _load_strategies(self):
        """
        Load strategies for current session and populate tabs.
        
        """
        try:
            session_id = self.selection_model.session_id
            if not session_id:
                log('DEBUG', 'No session selected - clearing strategy tabs',
                    category='strategies_view', action='load_strategies')
                self._clear_tabs()
                return
            
            # Get existing strategies for this session
            strategies = list(get_strategies(session_id))
            
            # Create default strategy if none exist
            if not strategies:
                log('INFO', 'No strategies found - creating default strategy',
                    category='strategies_view', action='load_strategies')
                default_strategy = self._on_create_strategy(name="Default")
                strategies = [default_strategy] if default_strategy else []
            
            self._clear_tabs()
            
            # Create tabs for existing strategies
            for strategy in strategies:
                tab = self._create_strategy_tab(strategy)
                self._add_tab(tab, strategy['name'])
            
        except Exception as e:
            log_exception(e, 'Failed to load strategies',
                         category='strategies_view', action='load_strategies')
    
    def _create_strategy_tab(self, strategy: dict) -> QWidget:
        """
        Create a tab widget for an existing strategy.
        
        Args:
            strategy: Strategy document from database with structure:
                {
                    '_id': ObjectId,
                    'name': str,
                    'model_data': {
                        'rows': [...],
                        'tires': {...}
                    }
                }
        
        Returns:
            StrategyTab widget with cloned table model
        """
        tab = StrategyTab(
            strategy=strategy,
            table_model=self.table_model,
            selection_model=self.selection_model
        )
        # keep track of name changes so the tab bar text stays in sync
        tab.name_changed.connect(lambda new_name, t=tab: self._update_tab_label(t, new_name))
        # when the tab requests deletion propagate it so we can remove it
        tab.deleted.connect(lambda sid, t=tab: self._remove_tab(t))
        return tab
    
    def _on_strategy_created(self, strategy: dict):
        """
        Handle strategy creation from MainTab.
        
        Args:
            strategy: Newly created strategy document
        """
        try:
            tab = self._create_strategy_tab(strategy)
            self._add_tab(tab, strategy['name'])
            
            log('INFO', f'Added tab for new strategy: {strategy["name"]}',
                category='strategies_view', action='on_strategy_created')
            
            # Emit signal for external listeners
            self.strategy_created.emit(strategy)
            
        except Exception as e:
            log_exception(e, 'Failed to create strategy tab',
                         category='strategies_view', action='on_strategy_created')
    
    def _on_create_strategy(self, name: str = None):
        """
        Handle strategy creation.
        
        Args:
            name: Optional strategy name. If not provided, generates "Strategy N" based on tab count.
        """
        try:
            strategy_name = name if name else f"Strategy {self.tab_bar.count() + 1}"
            
            # Get and sanitize table data
            row_data, tire_data, mean_stint_time = self.table_model.get_all_data()
            sanitized_data = sanitize_stints(row_data, tire_data)

            if not row_data:
                log('WARNING', 'No stint data to create strategy',
                    category='strategies_view', action='create_strategy')
                return
            
            if not self.selection_model.session_id:
                log('WARNING', 'No session selected',
                    category='strategies_view', action='create_strategy')
                return
            
            strategy = {
                "session_id": ObjectId(self.selection_model.session_id),
                "name": strategy_name,
                "model_data": sanitized_data,
                "mean_stint_time_seconds": int(mean_stint_time.total_seconds()) if mean_stint_time else 0
            }
            
            # Create strategy in database
            strategy_id = create_strategy(strategy)
            strategy['_id'] = strategy_id
            
            log('INFO', f'Strategy created: {strategy_name}',
                category='strategies_view', action='create_strategy')
            
            # Create tab for the new strategy
            tab = self._create_strategy_tab(strategy)
            self._add_tab(tab, strategy_name)
            
            # Emit signal for external listeners
            self.strategy_created.emit(strategy)
            
            return strategy
            
        except Exception as e:
            log_exception(e, 'Failed to create strategy',
                         category='strategies_view', action='create_strategy')
    
    def _on_session_changed(self, session_id=None, session_name=None):
        """Handle session change by reloading strategies.

        The sessionChanged signal provides two arguments (id and name) but
        they are not used here.  After the strategies list has been refreshed
        we also ensure the global loading overlay is hidden.  We look up the
        overlay via the active application window rather than relying on
        ``self.window()`` which may return ``None`` if the widget has not yet
        been attached to the main window.
        """
        from PyQt6.QtWidgets import QApplication

        # locate the application window
        app_window = self.window() or (QApplication.instance().activeWindow() if QApplication.instance() else None)
        log('DEBUG', 'Session changed - reloading strategies',
            category='strategies_view', action='on_session_changed')

        if app_window and hasattr(app_window, 'show_loading'):
            app_window.show_loading('Loading strategies for new session...')

        try:
            self._load_strategies()
        finally:
            if app_window and hasattr(app_window, 'hide_loading'):
                app_window.hide_loading()
    
    def _clear_tabs(self):
        """Remove all tabs from the tab bar and stacked widget."""
        while self.tab_bar.count() > 0:
            self.tab_bar.removeTab(0)
        
        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)

    def _remove_tab(self, widget: QWidget) -> None:
        """Remove a specific widget/tab from the interface.

        The caller usually passes the StrategyTab instance that emitted a
        deletion signal.  The method also calls ``deleteLater`` to help clean
        up resources.
        """
        index = self.stacked_widget.indexOf(widget)
        if index != -1:
            self.tab_bar.removeTab(index)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
            log('INFO', 'Removed strategy tab after deletion',
                category='strategies_view', action='remove_tab')
        else:
            log('WARNING', 'Attempted to remove non-existent tab',
                category='strategies_view', action='remove_tab')

    def _update_tab_label(self, widget: QWidget, new_label: str) -> None:
        """Update the tab bar text corresponding to a given widget.

        Args:
            widget: The widget that resides in ``self.stacked_widget``.
            new_label: The new label text to set on the tab bar.
        """
        index = self.stacked_widget.indexOf(widget)
        if index != -1:
            log('INFO', f'Updating tab label at index {index} to "{new_label}"',
                category='strategies_view', action='update_tab_label')
            self.tab_bar.setTabText(index, new_label)
            # some stylesheets or platform themes may not repaint automatically
            # after a text change, so force a refresh
            self.tab_bar.update()
            self.tab_bar.repaint()
        else:
            log('WARNING', 'Attempted to update label for non-existent tab',
                category='strategies_view', action='update_tab_label')
    
    def _add_tab(self, widget: QWidget, label: str):
        """
        Add a tab to both the tab bar and stacked widget.
        
        Args:
            widget: Widget to add as tab content
            label: Tab label text
        """
        self.tab_bar.addTab(label)
        self.stacked_widget.addWidget(widget)
