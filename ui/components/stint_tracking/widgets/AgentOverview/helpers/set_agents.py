from __future__ import annotations


def set_agents(self, agents: list[dict]) -> None:
    """Render a card for each agent and replace existing cards."""
    if self._cards_layout is None:
        return

    while self._cards_layout.count():
        item = self._cards_layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()

    for agent in agents:
        self._cards_layout.addWidget(self.AgentCard(agent))
