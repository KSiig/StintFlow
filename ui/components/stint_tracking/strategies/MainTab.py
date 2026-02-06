"""
Main strategy creation tab.

Allows users to create new race strategies by naming them and capturing
the current stint table state.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from bson import ObjectId
from core.errors import log, log_exception
from ui.models import ModelContainer
from ui.utilities import FONT, get_fonts
from core.utilities import resource_path


class MainTab(QWidget):
    """
    Strategy creation tab with input form and event stats.
    
    Left side: Form for creating a new strategy
    Right side: Event statistics (tires, race length)
    """
    
    strategy_created = pyqtSignal(dict)  # Emitted when strategy is created
    
    def __init__(self, models: ModelContainer):
        """
        Initialize the main strategy tab.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.inputs = {}
        
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self) -> None:
        """Load and apply navigation menu stylesheet."""
        try:
            with open(resource_path('resources/styles/main_tab.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'Navigation menu stylesheet not found', 
                         category='ui', action='load_stylesheet')
    
    def _setup_ui(self):
        """Set up the main layout with form and stats."""
        layout = QHBoxLayout(self)
        layout.addWidget(self._create_strategy_form())
        layout.addWidget(self._create_event_stats())
    
    def _create_strategy_form(self) -> QWidget:
        """
        Create the strategy input form.
        
        Returns:
            Widget containing the form fields and create button
        """
        frame = QFrame()
        frame.setObjectName("StrategyForm")
        frame.setFixedWidth(336)
        layout = QVBoxLayout(frame)
        
        # Form fields
        strategy_name = self._create_input_row(
            "strategy_name",
            "Strategy name",
            "Name to be used in the tab"
        )
        
        base_event = self._create_input_row(
            "base_event",
            "Base event",
            "Taken from session picker at top",
            text=self.selection_model.event_name,
            read_only=True
        )
        
        base_session = self._create_input_row(
            "base_session",
            "Base session",
            "Taken from session picker at top",
            text=self.selection_model.session_name,
            read_only=True
        )
        
        create_btn = self._create_submit_button()
        
        layout.addWidget(strategy_name)
        layout.addWidget(base_event)
        layout.addWidget(base_session)
        layout.addWidget(create_btn)
        layout.addStretch()
        
        return frame
    
    def _create_input_row(
        self,
        id: str,
        title: str,
        hint: str,
        text: str = "",
        read_only: bool = False
    ) -> QWidget:
        """
        Create an input row with title, hint, and text field.
        
        Args:
            id: Input identifier for storing reference
            title: Label text for the input
            hint: Hint/description text
            text: Default text value
            read_only: Whether input is read-only
            
        Returns:
            Widget containing the labeled input field
        """
        card = QFrame()
        card.setObjectName("SettingStrategy")
        card.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        card.setContentsMargins(0, 0, 0, 0)
        
        main_box = QVBoxLayout(card)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.setSpacing(0)
        
        # Labels
        title_label = QLabel(title)
        title_label.setObjectName("SettingTitle")
        title_label.setFont(get_fonts(FONT.header_input))
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        hint_label = QLabel(hint)
        hint_label.setObjectName("SettingHint")
        hint_label.setFont(get_fonts(FONT.header_input_hint))
        hint_label.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        hint_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hint_label.setContentsMargins(0, 0, 0, 8)
        
        # Input
        input_field = QLineEdit(text)
        input_field.setFont(get_fonts(FONT.text_small))
        input_field.setReadOnly(read_only)
        self.inputs[id] = input_field
        
        main_box.addWidget(title_label)
        main_box.addWidget(hint_label)
        main_box.addWidget(input_field)
        
        return card
    
    def _create_submit_button(self) -> QPushButton:
        """
        Create the strategy creation submit button.
        
        Returns:
            Configured submit button
        """
        btn = QPushButton("Create strategy")
        btn.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Minimum
        )
        btn.clicked.connect(self._on_create_strategy)
        
        return btn
    
    def _on_create_strategy(self):
        """
        Handle strategy creation button click.
        
        TODO: Implement strategy creation logic
        - Get table data using table_model.get_all_data()
        - Sanitize data using sanitize_stints()
        - Create strategy document
        - Call create_strategy() database function
        - Emit strategy_created signal
        """
        try:
            # TODO: Implement data extraction and sanitization
            # row_data, tire_data = self.table_model.get_all_data()
            # sanitized_data = sanitize_stints(row_data, tire_data)
            
            strategy_name = self.inputs['strategy_name'].text()
            
            if not strategy_name:
                log('WARNING', 'Strategy name is required',
                    category='main_tab', action='create_strategy')
                return
            
            strategy = {
                "session_id": ObjectId(self.selection_model.session_id),
                "name": strategy_name,
                # TODO: Add model_data from sanitized stints
                # "model_data": sanitized_data
            }
            
            # TODO: Call database create_strategy() function
            # from core.database import create_strategy
            # create_strategy(strategy)
            
            log('INFO', f'Strategy created: {strategy_name}',
                category='main_tab', action='create_strategy')
            
            # TODO: Emit signal when strategy creation is implemented
            # self.strategy_created.emit(strategy)
            
        except Exception as e:
            log_exception(e, 'Failed to create strategy',
                         category='main_tab', action='create_strategy')
    
    def _create_event_stats(self) -> QWidget:
        """
        Create the event statistics display.
        
        TODO: Implement stats display
        - Load event data using get_event()
        - Display tires available
        - Display race length
        
        Returns:
            Widget containing event statistics
        """
        frame = QFrame()
        layout = QGridLayout(frame)
        
        # TODO: Load event data and display stats
        # from core.database import get_event
        # event = get_event(self.selection_model.event_id)
        # 
        # tires_stat = self._create_stat_widget("Tires available", event['tires'])
        # length_stat = self._create_stat_widget("Race length", event['length'])
        # 
        # layout.addWidget(tires_stat, 0, 0, 
        #                 alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # layout.addWidget(length_stat, 1, 0,
        #                 alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # Placeholder
        placeholder = QLabel("Event stats")
        placeholder.setFont(get_fonts(FONT.header_input))
        layout.addWidget(placeholder, 0, 0,
                        alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout.setRowStretch(2, 1)
        
        return frame
    
    def _create_stat_widget(self, header: str, value: str) -> QWidget:
        """
        Create a single stat display widget.
        
        Args:
            header: Stat label
            value: Stat value
            
        Returns:
            Widget displaying the stat
        """
        frame = QFrame()
        frame.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Maximum
        )
        layout = QVBoxLayout(frame)
        
        lbl_header = QLabel(header)
        lbl_header.setFont(get_fonts(FONT.header_input))
        
        lbl_value = QLabel(value)
        lbl_value.setFont(get_fonts(FONT.text_small))
        
        layout.addWidget(lbl_header)
        layout.addWidget(lbl_value)
        
        return frame
