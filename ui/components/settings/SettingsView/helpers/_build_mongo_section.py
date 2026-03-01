"""Build the MongoDB settings section."""

from PyQt6.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout

from ui.utilities import FONT, get_fonts


def _build_mongo_section(self, parent_layout: QVBoxLayout) -> None:
    """Construct the MongoDB settings frame and add it to the parent layout."""
    mongo_frame = QFrame()
    mongo_frame.setObjectName("MongoFrame")
    mongo_layout = QVBoxLayout(mongo_frame)
    mongo_layout.setContentsMargins(0, 0, 0, 0)
    mongo_layout.setSpacing(12)

    mongo_title = QLabel("MongoDB")
    mongo_title.setFont(get_fonts(FONT.header_nav))
    mongo_layout.addWidget(mongo_title)

    form_layout = QFormLayout()
    form_layout.setContentsMargins(0, 0, 0, 0)
    form_layout.setSpacing(8)
    form_layout.setHorizontalSpacing(24)

    self._add_input(form_layout, "Connection string", "uri", "mongodb+srv://...")
    self._add_input(form_layout, "Host", "host", "localhost:27017")
    self._add_input(form_layout, "Database", "database", "stintflow")
    self._add_input(form_layout, "Username", "username", "")
    self._add_input(form_layout, "Password", "password", "", is_password=True)
    self._add_input(form_layout, "Auth source", "auth_source", "admin")

    mongo_layout.addLayout(form_layout)
    parent_layout.addWidget(mongo_frame)
