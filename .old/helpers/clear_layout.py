def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)

        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()

        # Handle nested layouts
        sub_layout = item.layout()
        if sub_layout is not None:
            clear_layout(sub_layout)