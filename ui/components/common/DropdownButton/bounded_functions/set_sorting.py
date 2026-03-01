"""Toggle sorting of dropdown entries."""


def set_sorting(self, enabled: bool) -> None:
    """Enable or disable alphabetical sorting and rebuild items."""
    self.sort_items = enabled
    self.set_items(self._raw_items)
