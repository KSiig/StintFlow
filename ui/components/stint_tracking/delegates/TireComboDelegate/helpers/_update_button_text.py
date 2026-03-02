"""Update the tire count button label."""

from ui.models.TableRoles import TableRoles


def _update_button_text(self, btn, index):
    tire_data = index.data(TableRoles.TiresRole)
    if tire_data:
        tires_changed = sum(tire_data["tires_changed"].values())
    else:
        tires_changed = 0
    btn.setText(str(tires_changed))
