"""LMU shared-memory helpers.

Provides a small context manager that yields an `LMUObjectOut` instance
backed by a memory-mapped file. Errors opening the shared memory are
logged via the project's error logger to aid debugging when the tracker
is launched as a separate process.
"""

from contextlib import contextmanager
import ctypes
import mmap
from typing import Iterator

from pyLMUSharedMemory import lmu_data
from core.errors import log_exception

# shared-memory tag constant simplifies mmap call and documents purpose
LMU_TAG = lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE


@contextmanager
def _open_lmu_shared_memory() -> Iterator["lmu_data.LMUObjectOut"]:
    """Yield an `LMUObjectOut` instance backed by platform shared memory.

    Yields:
        An `lmu_data.LMUObjectOut` instance providing `telemetry` and
        `scoring` attributes.

    Raises:
        OSError: Propagated after being logged when the underlying
            memory-mapping operation fails.
    """
    try:
        with mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(lmu_data.LMUObjectOut),
            tagname=LMU_TAG,
        ) as shared_mem:
            lmu = lmu_data.LMUObjectOut.from_buffer(shared_mem)
            yield lmu
    except Exception as e:  # pragma: no cover - platform-specific failures
        log_exception(e, "Failed to open LMU shared memory",
                      category="stint_tracker", action="open_lmu_shared_memory")
        raise