"""Configure the Python logging system once per process."""

import logging
import sys

from core.errors.get_log_file_path import get_log_file_path
from core.errors.log_rotation import parse_session_start, rotate_old_log, write_session_header
from .. import _state


def _configure_logger() -> None:
    """Configure file and console handlers with session-aware rotation."""
    if _state.logger_configured:
        return

    log_file = get_log_file_path()

    try:
        rotate_old_log(log_file)
    except Exception:
        # best-effort rotation; do not block startup
        pass

    logger = logging.getLogger("stintflow")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        _state.logger_configured = True
        return

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    try:
        if parse_session_start(log_file) is None:
            write_session_header(log_file)
    except Exception:
        pass

    _state.logger_configured = True
