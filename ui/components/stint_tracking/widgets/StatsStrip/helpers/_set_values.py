def _set_values(self) -> None:
    table_model = self.models.table_model

    self.longest_stint_card.refresh_value({"table_model": table_model})
    self.avg_stint_time_card.refresh_value({"table_model": table_model})
    self.stints_done_card.refresh_value({"table_model": table_model})
    self.tires_left_card.refresh_value({"table_model": table_model})
    self._refresh_driver_stats()