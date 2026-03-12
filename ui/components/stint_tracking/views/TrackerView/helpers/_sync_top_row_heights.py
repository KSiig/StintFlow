"""Keep the TrackerView top-row widgets at a matching height."""

from __future__ import annotations


def _sync_top_row_heights(self) -> None:
    """Apply the same fixed height to TableControls and StatsStrip."""
    table_controls = getattr(self, 'table_controls', None)
    stats_strip = getattr(self, 'stats_strip', None)
    if table_controls is None or stats_strip is None:
        return

    target_height = max(
        table_controls.sizeHint().height(),
        table_controls.minimumSizeHint().height(),
        stats_strip.sizeHint().height(),
        stats_strip.minimumSizeHint().height(),
    )
    if target_height <= 0:
        return

    table_controls.setFixedHeight(target_height)
    stats_strip.setFixedHeight(target_height)

    table_frame = getattr(table_controls, 'frame', None)
    if table_frame is not None:
        table_frame.setFixedHeight(target_height)

    stats_frame = getattr(stats_strip, '_frame', None)
    if stats_frame is not None:
        stats_frame.setFixedHeight(target_height)