from __future__ import annotations

from datetime import datetime, timedelta


def _set_status_color(self, heartbeat_dt) -> None:
	"""Set card status text and color based on heartbeat age."""
	self.status_text = 'Offline'
	self.status_color = '#374151'
	self.font_color = '#FFFFFF'

	if heartbeat_dt is None:
		return

	heartbeat_age = datetime.now(heartbeat_dt.tzinfo) - heartbeat_dt

	if heartbeat_age <= timedelta(seconds=15):
		self.status_text = 'Connected'
		self.status_color = '#386130'
		self.font_color = '#39FF14'
		return

	if heartbeat_age <= timedelta(minutes=1):
		self.status_text = 'Unavailable'
		self.status_color = '#85602c'
		self.font_color = '#FF9500'
		return

	self.status_text = 'Offline'
	self.status_color = '#374151'
	self.font_color = '#FFFFFF'
