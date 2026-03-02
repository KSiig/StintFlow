import sys
from pathlib import Path


def _should_show_restart(self) -> bool:
    """Show restart button only when running from a Python script."""
    script_path = Path(sys.argv[0]).resolve()
    return script_path.suffix.lower() == ".py"
