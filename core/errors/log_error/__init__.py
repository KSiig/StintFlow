"""Centralized logging entrypoints."""

from .log import log
from .log_exception import log_exception

__all__ = ["log", "log_exception"]
