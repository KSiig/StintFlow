from __future__ import annotations

from ...AgentCard import AgentCard


def set_agents(self, agents: list[dict]) -> None:
    """Populate the popup with cards for the connected agents."""
    cards_layout = getattr(self, "_cards_layout", None)
    if cards_layout is None:
        return
    while cards_layout.count():
        item = cards_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    for agent in agents:
        cards_layout.addWidget(AgentCard(agent))
    cards_layout.addStretch()
