from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle, QToolTip
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QRectF
from PyQt6.QtGui import QMouseEvent, QColor, QPixmap, QPainter
from ui.utilities.load_icon import load_icon
from PyQt6.QtSvg import QSvgRenderer
import os
from core.utilities import resource_path
from ui.models.TableRoles import TableRoles
from core.database import update_stint
from core.errors import log


class ActionsDelegate(QStyledItemDelegate):
    excludeClicked = pyqtSignal(int)
    # row index and optional strategy ID (empty string when not set)
    deleteClicked = pyqtSignal(int, str)
    buttonClicked = pyqtSignal(str, int)

    def __init__(self, parent=None, background_color: str = "#0e4c35", text_color: str = "#B0B0B0", update_doc: bool = False, strategy_id: str | None = None):
        """
        Initialize the delegate.
        
        Args:
            parent: Parent widget
            background_color: Hex color for pill background (default: dark green)
            text_color: Hex color for text (default: white)
            update_doc: Whether to persist changes to the database (default: False)
            strategy_id: Optional strategy ID for context when updating stints in database
        """
        super().__init__(parent)
        self.background_color = QColor(background_color)
        self.text_color = QColor(text_color)
        self.border_radius = 4
        # default button map: list of dicts with name and optional icon path
        self.button_width = 20
        self.spacing = 4
        self.buttons = [
            {"name": "exclude", "icon": "resources/icons/table_cells/circle.svg"},
            {"name": "delete", "icon": "resources/icons/table_cells/trash.svg"},
        ]
        self.update_doc = update_doc
        self.strategy_id = strategy_id

    def _draw_button(self, painter, style, rect: QRect, svg_name: str | None = None, text: str = "", excluded: bool = False):
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
            # allow override for excluded state (toggle icon)
            if svg_name.endswith('circle.svg') and excluded:
                svg_name = 'resources/icons/table_cells/circle-off.svg'

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
        x = option_rect.left() + self.spacing
        height = self.button_width
        y = option_rect.top() + option_rect.height() // 2 - height // 2

        for _ in self.buttons:
            rects.append(QRect(x, y, self.button_width, height))
            x += self.button_width + self.spacing

        return rects

    def helpEvent(self, event, view, option, index):
        """Show configurable tooltips for buttons when hovered.

        The `buttons` map may include a `tooltip` entry which can be a string
        or a dict with keys `included`/`excluded` to provide state-dependent text.
        """
        try:
            pos = event.pos()
        except Exception:
            return super().helpEvent(event, view, option, index)

        rects = self._button_rects(option.rect)
        row = index.row()
        model = index.model()
        meta = None
        if model is not None:
            meta = model.data(model.index(row, 0), TableRoles.MetaRole)
        excluded = bool(meta.get('excluded')) if isinstance(meta, dict) else False
        for btn, rect in zip(self.buttons, rects):
            if rect.contains(pos):
                tip = btn.get('tooltip')
                name = btn.get('name', '')

                # Resolve tooltip value
                if isinstance(tip, dict):
                    # support keys 'included'/'excluded' for stateful tooltips
                    if name == 'exclude':
                        if excluded:
                            text = tip.get('excluded') or tip.get('off') or tip.get('included')
                        else:
                            text = tip.get('included') or tip.get('on') or tip.get('excluded')
                    else:
                        text = tip.get('text') or ''
                elif isinstance(tip, str):
                    text = tip
                else:
                    # default tooltips
                    if name == 'exclude':
                        text = 'Include in mean' if excluded else 'Exclude from mean'
                    else:
                        text = name.capitalize()

                if text:
                    QToolTip.showText(event.globalPos(), text, view)
                    return True

        return super().helpEvent(event, view, option, index)

    def paint(self, painter, option, index):
        """Draw buttons inside the cell."""

        # Let Qt draw background (selection, etc.)
        super().paint(painter, option, index)

        # Calculate button rectangles for configured buttons
        rects = self._button_rects(option.rect)
        style = option.widget.style()

        row = index.row()
        model = index.model()
        # fetch meta for this row via MetaRole (model returns None if missing)
        meta = None
        if model is not None:
            meta = model.data(model.index(row, 0), TableRoles.MetaRole)
        excluded = bool(meta.get('excluded')) if isinstance(meta, dict) else False

        for btn, rect in zip(self.buttons, rects):
            svg = btn.get("icon")
            text = btn.get("name", "")
            self._draw_button(painter, style, rect, svg_name=svg, text="" if svg else text, excluded=excluded)

    def editorEvent(self, event, model, option, index):
        """Handle mouse click events by delegating to helpers."""

        if event.type() == event.Type.MouseButtonRelease:
            # debug log left in place to aid manual testing
            if isinstance(event, QMouseEvent):
                return self._handle_mouse_click(event, model, option, index)
        return False

    # ------------------------------------------------------------------
    # Private helpers for editorEvent
    # ------------------------------------------------------------------

    def _handle_mouse_click(self, event, model, option, index) -> bool:
        """Process a mouse release and dispatch to the appropriate button.

        Returns ``True`` if one of the buttons was activated (so the view
        knows the event was consumed).
        """
        pos = event.position().toPoint()
        rects = self._button_rects(option.rect)

        for i, rect in enumerate(rects):
            if rect.contains(pos):
                name = self.buttons[i].get("name", "")
                row = index.row()
                if name == "exclude" and model is not None:
                    self._toggle_exclude(row, model, option)
                self._emit_button_signals(name, row)
                return True
        return False

    def _toggle_exclude(self, row: int, model, option) -> None:
        """Flip the excluded flag for *row* and update associated state."""
        meta = model.data(model.index(row, 0), TableRoles.MetaRole) or {}
        if not isinstance(meta, dict):
            meta = {}
        meta['excluded'] = not bool(meta.get('excluded'))
        model.setData(model.index(row, 0), meta, role=TableRoles.MetaRole)

        # request view repaint
        if option.widget is not None:
            option.widget.viewport().update()

        # Recalculate mean in-model.  If model represents a strategy the
        # pending rows should not be regenerated, so we pass the flag
        # accordingly.
        try:
            if hasattr(model, 'update_mean'):
                is_strat = getattr(model, '_is_strategy', False)
                model.update_mean(update_pending=not is_strat)
        except Exception:
            pass

        # Persist excluded flag to database if requested
        if self.update_doc:
            self._persist_excluded_flag(meta)

    def _persist_excluded_flag(self, meta: dict) -> None:
        """Write the excluded state back to the database.

        This method is separated out so that the calling code can be
        easier to test and so persistence logic is confined in one place.
        """
        try:
            stint_id = meta.get('id')
            if stint_id:
                update_stint(str(stint_id), {"excluded": bool(meta.get('excluded'))})
        except Exception as e:
            log('ERROR', f'Failed to persist excluded flag for stint {stint_id}: {e}',
                category='actions_delegate', action='persist_excluded')

    def _emit_button_signals(self, name: str, row: int) -> None:
        """Emit the generic ``buttonClicked`` signal and any specific ones."""
        self.buttonClicked.emit(name, row)
        if name == "exclude":
            self.excludeClicked.emit(row)
        elif name == "delete":
            self.deleteClicked.emit(row, self.strategy_id if self.strategy_id else "")
