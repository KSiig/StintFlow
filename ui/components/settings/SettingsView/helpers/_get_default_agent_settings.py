"""Defaults for agent settings."""

import os
import socket


def _get_default_agent_settings(self) -> dict:
    """Return default agent-related settings."""
    default_name = os.getenv("AGENT_NAME", "")
    if not default_name:
        try:
            default_name = socket.gethostname()
        except Exception:
            default_name = ""

    return {"name": default_name}
