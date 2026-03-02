"""Utilities for loading QSS stylesheets for UI components.

The public function `load_style` takes a single argument `file_name` which
is the resource-relative path to the stylesheet (for example:
`resources/styles/common/config_button.qss`). When logging, the `file_name` is
used as the `category` with `/` replaced by `-`.
"""
from core.utilities import resource_path
from core.errors import log, log_exception


def load_style(file_name: str, widget=None) -> str:
    """Return the stylesheet contents; optionally apply it to `widget`.

    If `widget` is provided the function will attempt to call
    `widget.setStyleSheet(style)` and will log any exceptions. The
    `file_name` is used as the logging category with `/` replaced by
    `-`.
    """
    try:
        with open(resource_path(file_name), 'r', encoding='utf-8') as f:
            style = f.read()
    except FileNotFoundError:
        category = file_name.replace('/', '-')
        log('WARNING', f'{file_name} stylesheet not found', category=category, action='load_stylesheet')
        return ""

    if widget and style:
        try:
            widget.setStyleSheet(style)
        except Exception as e:
            category = file_name.replace('/', '-')
            log_exception(e, 'Failed to apply stylesheet', category=category, action='apply_stylesheet')

    return style
