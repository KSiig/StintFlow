"""Build the save/reload button row."""

from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout


def _build_button_section(self, parent_layout: QVBoxLayout) -> None:
    """Construct the save/reload button row."""
    button_layout = QHBoxLayout()
    button_layout.setSpacing(8)

    save_button = QPushButton("Save")
    self.reload_button = QPushButton("Reload")
    save_button.clicked.connect(self._save_settings)
    self.reload_button.clicked.connect(self._restart_app)

    button_layout.addWidget(save_button)
    button_layout.addWidget(self.reload_button)
    button_layout.addStretch()
    self.reload_button.hide()

    parent_layout.addLayout(button_layout)
