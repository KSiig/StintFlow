import sys
from pathlib import Path


def _get_restart_command(self) -> tuple[str, list[str]]:
    """Build the restart command for script or bundled executable."""
    executable = sys.executable
    script_path = Path(sys.argv[0]).resolve()

    if script_path.suffix.lower() == ".py":
        return executable, [str(script_path), *sys.argv[1:]]

    return executable, list(sys.argv[1:])
