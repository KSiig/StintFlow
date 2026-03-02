def set_sorting(self, enabled: bool) -> None:
    """Enable or disable alphabetical sorting of the entries.

    This will reorder the internal item list and refresh the popup.
    """
    self._sort_items = enabled
    self.dropdown.set_sorting(enabled)
    self._refresh_items()