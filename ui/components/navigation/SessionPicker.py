"""
Session picker component for event and session selection.

Displays dropdown boxes for selecting an event and its associated session.
Updates when selections change and maintains synchronization with the
selection model.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from pymongo.errors import PyMongoError

from ui.utilities import FONT, get_fonts, get_cached_icon
from ui.models import ModelContainer
from core.utilities import resource_path
from core.errors import log, log_exception
from core.database import get_events, get_sessions
from ..common import UpwardComboBox
from .constants import (
    FRAME_TOP_MARGIN,
    FRAME_BOTTOM_MARGIN,
    FRAME_LEFT_MARGIN,
    FRAME_RIGHT_MARGIN,
    COMBO_SPACING,
    COMBO_HEIGHT,
    ICON_SIZE,
    ICON_COLOR,
    ICON_X_POSITION,
    ICON_Y_POSITION,
    ICON_CALENDAR,
    ICON_CLOCK
)


class SessionPicker(QWidget):
    """
    Event and session selection widget.
    
    Provides combo boxes for selecting race events and their associated sessions.
    Automatically updates the session list when a new event is selected.
    Maintains synchronization with the SelectionModel.
    """
    
    def __init__(self, models: ModelContainer = None) -> None:
        """
        Initialize the session picker.
        
        Args:
            models: Container with selection_model for tracking event/session selections
        """
        super().__init__()
        self.models = models
        self.selection_model = models.selection_model if models else None
        
        self._setup_styles()
        self._create_layout()
        self._populate_initial_data()
    
    def _setup_styles(self) -> None:
        """Load and apply session picker stylesheet."""
        try:
            with open(resource_path('resources/styles/session_picker.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'Session picker stylesheet not found', 
                         category='ui', action='load_stylesheet')
        
        self.setObjectName("StintSelection")
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Maximum
        )
    
    def _create_layout(self) -> None:
        """Create and configure the session picker layout with combo boxes."""
        # Container frame
        frame = QFrame()
        frame.setObjectName("ComboBoxes")
        frame.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed
        )
        frame.setContentsMargins(0, FRAME_TOP_MARGIN, 0, FRAME_BOTTOM_MARGIN)
        
        # Root layout
        root_widget_layout = QVBoxLayout(self)
        root_widget_layout.setContentsMargins(0, 0, 0, 0)
        root_widget_layout.addWidget(frame)
        
        # Frame layout
        root_layout = QVBoxLayout(frame)
        root_layout.setContentsMargins(FRAME_LEFT_MARGIN, 0, FRAME_RIGHT_MARGIN, 0)
        root_layout.setSpacing(COMBO_SPACING)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Create combo boxes
        self.events = self._create_combo_box()
        self.sessions = self._create_combo_box()
        
        # Connect signals
        self.events.currentIndexChanged.connect(self._on_event_changed)
        self.sessions.currentIndexChanged.connect(self._on_session_changed)
        
        # Add icons to combo boxes
        self._add_combo_icon(self.events, ICON_CALENDAR)
        self._add_combo_icon(self.sessions, ICON_CLOCK)
        
        # Add combo boxes to layout
        root_layout.addWidget(self.events)
        root_layout.addWidget(self.sessions)
    
    def _create_combo_box(self) -> UpwardComboBox:
        """
        Create a configured combo box for the session picker.
        
        Returns:
            Configured UpwardComboBox with standard styling and properties
        """
        combo = UpwardComboBox()
        combo.setEditable(False)
        combo.setObjectName("ComboBox")
        combo.setFont(get_fonts(FONT.combo_input))
        combo.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed
        )
        combo.setFixedHeight(COMBO_HEIGHT)
        combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        return combo
    
    def _add_combo_icon(self, combo_box: UpwardComboBox, icon_path: str) -> None:
        """
        Add an icon to a combo box positioned inside the left edge.
        
        Creates a label widget as a child of the combo box and positions it
        absolutely at the left edge. The icon is cached for efficient reuse.
        
        Args:
            combo_box: The combo box to add the icon to
            icon_path: Path to the SVG icon file
        """
        icon_pixmap = get_cached_icon(icon_path, ICON_SIZE, ICON_COLOR)
        
        icon_label = QLabel(combo_box)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(ICON_SIZE, ICON_SIZE)
        icon_label.move(ICON_X_POSITION, ICON_Y_POSITION)
        icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    
    def _populate_initial_data(self) -> None:
        """
        Populate combo boxes with initial data from database.
        
        Loads events and sessions, then sets the initial selection based
        on the selection model if available.
        """
        self._load_events()
        
        # Load initial sessions for first event
        if self.events.count() > 0:
            self._populate_sessions(self.events.currentData())
        
        # Set initial selection from model
        self._apply_selection_from_model()
    
    def _load_events(self) -> None:
        """
        Load all events from database into the events combo box.
        
        Clears existing items and repopulates with all available events.
        Logs success/failure for debugging.
        """
        try:
            events = get_events(sort_by=None)
            
            for doc in events:
                self.events.addItem(doc["name"], userData=str(doc["_id"]))
            
            log('DEBUG', f'Loaded {len(events)} events into combo box', 
                category='ui', action='load_events')
                
        except PyMongoError as e:
            log_exception(e, 'Failed to load events from database', 
                         category='ui', action='load_events')
        except Exception as e:
            log_exception(e, 'Unexpected error loading events', 
                         category='ui', action='load_events')
    
    def _apply_selection_from_model(self) -> None:
        """
        Apply event and session selection from the selection model.
        
        If the selection model has stored event/session IDs, sets the
        combo boxes to those selections.
        """
        if not self.selection_model:
            return
        
        event_id = self.selection_model.event_id
        session_id = self.selection_model.session_id
        
        if event_id:
            event_index = self.events.findData(str(event_id))
            if event_index >= 0:
                self.events.setCurrentIndex(event_index)
        
        if session_id:
            session_index = self.sessions.findData(str(session_id))
            if session_index >= 0:
                self.sessions.setCurrentIndex(session_index)
    
    def _populate_sessions(self, event_id: str = None) -> None:
        """
        Populate the sessions combo box for a specific event.
        
        Args:
            event_id: The event ID to load sessions for (None to clear sessions)
        """
        self.sessions.blockSignals(True)
        self.sessions.clear()
        
        # Validate event_id before querying
        if not event_id:
            self.sessions.blockSignals(False)
            return
        
        try:
            sessions = get_sessions(event_id, sort_by=None)
            
            for doc in sessions:
                self.sessions.addItem(doc["name"], userData=str(doc["_id"]))
            
            log('DEBUG', f'Loaded {len(sessions)} sessions for event {event_id}', 
                category='ui', action='populate_sessions')
                
        except ValueError as e:
            log_exception(e, f'Invalid event ID: {event_id}', 
                         category='ui', action='populate_sessions')
        except PyMongoError as e:
            log_exception(e, f'Failed to load sessions for event {event_id}', 
                         category='ui', action='populate_sessions')
        except Exception as e:
            log_exception(e, f'Unexpected error loading sessions for event {event_id}', 
                         category='ui', action='populate_sessions')
        finally:
            self.sessions.blockSignals(False)
    
    def _on_event_changed(self) -> None:
        """
        Handle event selection change.
        
        Updates the sessions combo box and selection model when a new event is selected.
        """
        event_id = self.events.currentData()
        event_name = self.events.currentText()
        
        if self.selection_model:
            self.selection_model.set_event(event_id, event_name)
        
        # Repopulate sessions
        self._populate_sessions(event_id)
        
        # Set model to first session by default
        if self.sessions.count() > 0 and self.selection_model:
            self.selection_model.set_session(
                self.sessions.currentData(), 
                self.sessions.currentText()
            )
        elif self.selection_model:
            self.selection_model.set_session(None)
    
    def _on_session_changed(self) -> None:
        """
        Handle session selection change.
        
        Updates the selection model when a new session is selected.
        """
        if self.selection_model:
            self.selection_model.set_session(
                self.sessions.currentData(), 
                self.sessions.currentText()
            )
    
    def reload(self, selected_event_id: str = None, selected_session_id: str = None) -> None:
        """
        Refresh events and sessions combo boxes.
        
        Reloads all data from the database and optionally selects specific items.
        
        Args:
            selected_event_id: Event ID to select after reload (optional)
            selected_session_id: Session ID to select after reload (optional)
        """
        self.events.blockSignals(True)
        self.sessions.blockSignals(True)
        
        # Refresh events
        self.events.clear()
        self._load_events()
        
        # Determine which event to select
        target_event_id = selected_event_id
        if not target_event_id and self.selection_model and self.selection_model.event_id:
            target_event_id = str(self.selection_model.event_id)
        
        # Select event
        if target_event_id:
            index = self.events.findData(target_event_id)
            if index >= 0:
                self.events.setCurrentIndex(index)
        
        # Refresh sessions for selected event
        event_id = self.events.currentData()
        self.sessions.clear()
        if event_id:
            self._populate_sessions(event_id)
        
        # Determine which session to select
        target_session_id = selected_session_id
        if not target_session_id and self.selection_model and self.selection_model.session_id:
            target_session_id = str(self.selection_model.session_id)
        
        # Select session
        if target_session_id:
            index = self.sessions.findData(target_session_id)
            if index >= 0:
                self.sessions.setCurrentIndex(index)
        
        # Update selection model to match combo boxes
        if self.selection_model:
            self.selection_model.set_event(self.events.currentData(), self.events.currentText())
            self.selection_model.set_session(self.sessions.currentData(), self.sessions.currentText())
        
        self.sessions.blockSignals(False)
        self.events.blockSignals(False)
