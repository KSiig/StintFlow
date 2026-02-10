"""
Resolve the command used to launch the stint tracker process.
"""

from __future__ import annotations

import sys
from pathlib import Path

from core.errors import log


def get_stint_tracker_command() -> tuple[str, list[str]]:
    """Return the program and base args for launching the stint tracker."""
    if getattr(sys, "frozen", False):
        executable_dir = Path(sys.executable).resolve().parent
        processor_exe = executable_dir / "StintTracker.exe"
        if processor_exe.exists():
            return str(processor_exe), []

        log(
            "WARNING",
            "StintTracker.exe not found; falling back to Python script",
            category="stint_tracker",
            action="resolve_command",
        )

    project_root = Path(__file__).resolve().parents[2]
    script_path = project_root / "processors" / "stint_tracker" / "run.py"
    return "python3", ["-u", str(script_path)]
