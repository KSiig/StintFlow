from ui.components.stint_tracking import get_header_titles
from ui.models import TableModel
from ui.utilities.initialization_worker import InitializationWorker


def _start_initialization(self) -> None:
    """Begin asynchronous view/data setup via worker thread."""
    self.table_model = TableModel(
        selection_model=self.selection_model,
        headers=get_header_titles(),
        load_on_init=False,
    )

    if hasattr(self, "loading_overlay") and self.loading_overlay:
        self.loading_overlay.set_status("Initializing...")

    self._init_worker = InitializationWorker(self.selection_model)
    self._init_worker.status.connect(self._on_status_update)
    self._init_worker.connectionFailed.connect(self._on_connection_failed)
    self._init_worker.finished.connect(self._on_initialization_done)
    self._init_worker.start()
