from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QRectF
from PyQt6.QtGui import QMouseEvent, QColor, QPixmap, QPainter
from ui.utilities.load_icon import load_icon
from PyQt6.QtSvg import QSvgRenderer
import os
from core.utilities import resource_path


class ActionsDelegate(QStyledItemDelegate):
    editClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)
    buttonClicked = pyqtSignal(str, int)

    def __init__(self, parent=None, background_color: str = "#0e4c35", text_color: str = "#B0B0B0"):
        """
        Initialize the delegate.
        
        Args:
            parent: Parent widget
            background_color: Hex color for pill background (default: dark green)
            text_color: Hex color for text (default: white)
        """
        super().__init__(parent)
        self.background_color = QColor(background_color)
        self.text_color = QColor(text_color)
        self.border_radius = 4
        # default button map: list of dicts with name and optional icon path
        self.button_width = 20
        self.spacing = 4
        self.left_margin = 20
        self.buttons = [
            {"name": "edit", "icon": "resources/icons/race_config/square-pen.svg"},
            {"name": "delete", "icon": "resources/icons/race_config/square-pen.svg"},
        ]

    def _draw_button(self, painter, style, rect: QRect, svg_name: str | None = None, text: str = ""):
        """Private helper: draw a push button (background) and optionally an SVG icon or text.

        Args:
            painter: QPainter instance
            style: widget style to draw the button background
            rect: QRect where the button should be drawn
            svg_name: resource path (relative) to an SVG to render inside the button
            text: fallback text to draw if no svg is provided or found
        """
        # Transparent background: do not draw the standard pushbutton background
        # (we only render icon/text so the button area appears transparent)

        # Draw icon or text
        if svg_name:
            icon_size = int(min(rect.width(), rect.height()) - 6)
            icon_x = rect.left() + (rect.width() - icon_size) // 2
            icon_y = rect.top() + (rect.height() - icon_size) // 2

            # Use shared utility to load + colorize icon
            pix = load_icon(svg_name, size=icon_size, color=self.text_color.name())
            if not pix.isNull():
                painter.drawPixmap(int(icon_x), int(icon_y), pix)
                return

        # fallback: draw text if provided, otherwise a small placeholder
        painter.save()
        if text:
            painter.setPen(self.text_color)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        else:
            painter.setPen(Qt.GlobalColor.red)
            painter.drawRect(rect.adjusted(4, 4, -4, -4))
        painter.restore()

    def _button_rects(self, option_rect: QRect):
        """Compute and return a list of QRect for each configured button.

        Rects are horizontally laid out starting from the left edge with `self.spacing`.
        """
        rects = []
        x = option_rect.left() + self.left_margin + self.spacing
        height = self.button_width
        y = option_rect.top() + option_rect.height() // 2 - height // 2

        for _ in self.buttons:
            rects.append(QRect(x, y, self.button_width, height))
            x += self.button_width + self.spacing

        return rects

    def paint(self, painter, option, index):
        """Draw buttons inside the cell."""

        # Let Qt draw background (selection, etc.)
        super().paint(painter, option, index)

        # Calculate button rectangles for configured buttons
        rects = self._button_rects(option.rect)
        style = option.widget.style()

        for btn, rect in zip(self.buttons, rects):
            svg = btn.get("icon")
            text = btn.get("name", "")
            self._draw_button(painter, style, rect, svg_name=svg, text="" if svg else text)

    def editorEvent(self, event, model, option, index):
        """Handle mouse click events."""

        if event.type() == event.Type.MouseButtonRelease:
            if isinstance(event, QMouseEvent):
                pos = event.position().toPoint()

                rects = self._button_rects(option.rect)
                for i, rect in enumerate(rects):
                    if rect.contains(pos):
                        name = self.buttons[i].get("name", "")
                        # emit both generic and specific signals when applicable
                        self.buttonClicked.emit(name, index.row())
                        if name == "edit":
                            self.editClicked.emit(index.row())
                        elif name == "delete":
                            self.deleteClicked.emit(index.row())
                        return True

        return False
