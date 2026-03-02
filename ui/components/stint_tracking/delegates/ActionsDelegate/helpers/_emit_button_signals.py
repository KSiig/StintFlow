"""Emit button signals for action clicks."""


def _emit_button_signals(self, name: str, row: int) -> None:
    self.buttonClicked.emit(name, row)
    if name == "exclude":
        self.excludeClicked.emit(row)
    elif name == "delete":
        self.deleteClicked.emit(row, self.strategy_id if self.strategy_id else "")
