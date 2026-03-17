from __future__ import annotations

from PyQt6.QtWidgets import QVBoxLayout

from ui.components.common import LabeledInputRow
from ....config import ConfigLayout
from ...TeamSection import TeamSection
from ._on_text_changed import _on_text_changed


def _add_config_rows(self, layout: QVBoxLayout) -> None:
    """Add labeled inputs and team section to the layout."""
    for field_id, title in [
        ("event_name", "Event name"),
        ("session_name", "Session name"),
        ("tires", "Starting tires"),
        ("length", "Race length"),
        ("start_time", "Start time"),
        ("tires_remaining_at_green_flag", "Tires at green flag"),
    ]:
        card = LabeledInputRow(
            title=title, 
            input_height=ConfigLayout.INPUT_HEIGHT, 
            on_text_change=lambda: _on_text_changed(self)
        )
        self.inputs[field_id] = card.get_input_field()
        layout.addWidget(card)

    self.team_section = TeamSection(on_change=lambda: _on_text_changed(self))
    self.driver_inputs = self.team_section.get_driver_inputs()
    self.drivers = self.team_section.get_driver_names()
    layout.addWidget(self.team_section)
