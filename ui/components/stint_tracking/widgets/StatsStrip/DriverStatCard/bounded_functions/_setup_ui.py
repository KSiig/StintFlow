"""Build the DriverStatCard UI."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, QSizePolicy, QVBoxLayout


def _setup_ui(self) -> None:
    """Create the driver stat card layout and child widgets."""
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    self.setFixedHeight(44)

    layout = QHBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    self.initials_label = QLabel(self)
    self.initials_label.setObjectName('DriverStatCardInitials')
    self.initials_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.initials_label.setFont(self.initials_font)
    self.initials_label.setFixedSize(44, 44)
    layout.addWidget(self.initials_label)

    details_layout = QVBoxLayout()
    details_layout.setContentsMargins(0, 2, 0, 2)
    details_layout.setSpacing(6)

    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(8)

    self.driver_name_label = QLabel(self)
    self.driver_name_label.setObjectName('DriverStatCardName')
    self.driver_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    self.driver_name_label.setFont(self.driver_name_font)
    header_layout.addWidget(self.driver_name_label)

    header_layout.addStretch()

    self.stint_count_label = QLabel(self)
    self.stint_count_label.setObjectName('DriverStatCardStints')
    self.stint_count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    self.stint_count_label.setFont(self.stint_count_font)
    header_layout.addWidget(self.stint_count_label)

    details_layout.addLayout(header_layout)

    footer_layout = QHBoxLayout()
    footer_layout.setContentsMargins(0, 0, 0, 0)
    footer_layout.setSpacing(8)

    self.progress_bar = QProgressBar(self)
    self.progress_bar.setObjectName('DriverStatCardProgressBar')
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setTextVisible(False)
    self.progress_bar.setFixedHeight(4)
    self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    footer_layout.addWidget(self.progress_bar)

    self.total_time_label = QLabel(self)
    self.total_time_label.setObjectName('DriverStatCardTime')
    self.total_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    self.total_time_label.setFont(self.total_time_font)
    footer_layout.addWidget(self.total_time_label)

    details_layout.addLayout(footer_layout)

    details_frame = QFrame(self)
    details_frame.setObjectName('DriverStatCardDetails')
    details_frame.setLayout(details_layout)
    details_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    layout.addWidget(details_frame)