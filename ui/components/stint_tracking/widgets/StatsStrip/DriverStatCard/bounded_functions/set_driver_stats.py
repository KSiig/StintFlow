"""Apply driver statistics to a DriverStatCard instance."""


def set_driver_stats(
    self,
    driver_name: str,
    stint_count: int,
    total_time_text: str,
    progress_value: int,
) -> None:
    """Update the card labels and progress bar with driver data."""
    cleaned_name = str(driver_name).strip() or 'Unknown driver'
    cleaned_stint_count = max(int(stint_count), 0)
    cleaned_time_text = str(total_time_text).strip() or '00:00:00'
    clamped_progress = max(0, min(int(progress_value), 100))

    initials_parts = [part[0].upper() for part in cleaned_name.split() if part]
    initials = ''.join(initials_parts[:2]) or '?'
    stint_label = 'stint' if cleaned_stint_count == 1 else 'stints'

    self.driver_name = cleaned_name
    self.stint_count = cleaned_stint_count
    self.total_time_text = cleaned_time_text
    self.progress_value = clamped_progress

    if self.initials_label is not None:
        self.initials_label.setText(initials)

    if self.driver_name_label is not None:
        self.driver_name_label.setText(cleaned_name)

    if self.stint_count_label is not None:
        self.stint_count_label.setText(f'{cleaned_stint_count} {stint_label}')

    if self.total_time_label is not None:
        self.total_time_label.setText(cleaned_time_text)

    if self.progress_bar is not None:
        self.progress_bar.setValue(clamped_progress)