"""Reload events and sessions combo boxes."""


def reload(self, selected_event_id: str = None, selected_session_id: str = None) -> None:
	"""Refresh events and sessions combo boxes."""
	self.events.blockSignals(True)
	self.sessions.blockSignals(True)

	self.events.clear()
	self._load_events()

	target_event_id = selected_event_id
	if not target_event_id and self.selection_model and self.selection_model.event_id:
		target_event_id = str(self.selection_model.event_id)

	if target_event_id:
		index = self.events.findData(target_event_id)
		if index >= 0:
			self.events.setCurrentIndex(index)

	event_id = self.events.currentData()
	self.sessions.clear()
	if event_id:
		self._populate_sessions(event_id)

	target_session_id = selected_session_id
	if not target_session_id and self.selection_model and self.selection_model.session_id:
		target_session_id = str(self.selection_model.session_id)

	if target_session_id:
		index = self.sessions.findData(target_session_id)
		if index >= 0:
			self.sessions.setCurrentIndex(index)

	if self.selection_model:
		self.selection_model.set_event(self.events.currentData(), self.events.currentText())
		self.selection_model.set_session(self.sessions.currentData(), self.sessions.currentText())

	self.sessions.blockSignals(False)
	self.events.blockSignals(False)
