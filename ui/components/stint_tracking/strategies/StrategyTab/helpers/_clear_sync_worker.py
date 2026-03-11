"""Clear the active strategy sync worker reference."""

from __future__ import annotations


from __future__ import annotations


def _clear_sync_worker(self, worker: object | None = None) -> None:
    """Forget the current sync worker after it finishes.

    The `finished` signal may fire for an old worker after a new one has been
    started.  If we simply clear the attribute unconditionally the newer
    instance would be dropped and we could leak or mis-handle the still-
    running worker.  We compare the sender (or the passed-in worker) against
    ``self._sync_worker`` and only clear when they are identical.
    """
    # if the slot was invoked via a lambda, we receive the worker as an
    # argument.  otherwise fall back to QObject.sender()
    if worker is None:
        try:
            # pylint: disable=no-member
            worker = self.sender()
        except Exception:  # sender may not exist outside of Qt context
            worker = None
    if worker is self._sync_worker:
        self._sync_worker = None
