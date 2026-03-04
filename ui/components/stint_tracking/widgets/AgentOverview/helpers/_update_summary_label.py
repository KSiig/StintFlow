from __future__ import annotations


def _update_summary_label(self, agents: list[dict]) -> None:
    """Update the summary label with the current agent count."""
    label = getattr(self, "_summary_label", None)
    total = len(agents)
    if label is not None:
        if total == 0:
            label.setText("0 / 0 agents")
        else:
            label.setText(f"{total} / {total} agent{'s' if total != 1 else ''}")
