"""Compact card widget for per-driver stint statistics."""

from PyQt6.QtWidgets import QFrame

from ui.utilities import FONT, get_fonts
from ui.utilities.load_style import load_style

from .bounded_functions import _setup_ui, set_driver_stats


class DriverStatCard(QFrame):
    """Display a driver's initials, stint count, and share of total drive time."""

    _setup_ui = _setup_ui
    set_driver_stats = set_driver_stats

    def __init__(
        self,
        driver_name: str,
        stint_count: int = 0,
        total_time_text: str = '00:00:00',
        progress_value: int = 0,
    ) -> None:
        super().__init__()

        load_style('resources/styles/stint_tracking/tracker/driver_stat_card.qss', widget=self)
        self.setObjectName('DriverStatCard')

        self.driver_name = driver_name
        self.stint_count = stint_count
        self.total_time_text = total_time_text
        self.progress_value = progress_value

        self.initials_label = None
        self.driver_name_label = None
        self.stint_count_label = None
        self.progress_bar = None
        self.total_time_label = None

        self.initials_font = get_fonts(FONT.text_label_bold)
        self.driver_name_font = get_fonts(FONT.text_label_bold)
        self.stint_count_font = get_fonts(FONT.text_caption)
        self.total_time_font = get_fonts(FONT.text_caption)

        self._setup_ui()
        self.set_driver_stats(driver_name, stint_count, total_time_text, progress_value)