from ui.components.common import DraggableArea
from ui.components.navigation import NavigationMenu
from ui.components.window.WindowButtons import WindowButtons
from ui.models import ModelContainer

from ...layout_factory import create_scroll_area, create_stacked_container


def _create_components(self) -> None:
    """Create navigation, controls, and central container components."""
    models = ModelContainer(
        selection_model=self.selection_model,
        navigation_model=self.navigation_model,
    )

    self.navigation_menu = NavigationMenu(self, models=models)
    self.window_buttons = WindowButtons(self)
    self.draggable_area = DraggableArea(self)

    self.central_scroll_area = create_scroll_area()
    self.central_container, self.central_container_layout = create_stacked_container(self.central_scroll_area)

    self.navigation_model.activeWidgetChanged.connect(self._change_workspace_widget)
