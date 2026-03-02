from ...layout_factory import create_main_layout, create_right_pane


def _assemble_layout(self) -> None:
    """Assemble all layout components into the main window."""
    right_pane = create_right_pane(self.central_scroll_area)
    border_frame = create_main_layout(self.navigation_menu, right_pane)
    self.setCentralWidget(border_frame)
