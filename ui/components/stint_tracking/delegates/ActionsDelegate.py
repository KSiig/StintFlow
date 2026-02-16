from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QMouseEvent


class ActionsDelegate(QStyledItemDelegate):
    editClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)

    def paint(self, painter, option, index):
        """Draw buttons inside the cell."""

        # Let Qt draw background (selection, etc.)
        super().paint(painter, option, index)

        # Calculate button geometry
        button_width = 60
        spacing = 5
        height = option.rect.height() - 6

        edit_rect = QRect(
            option.rect.left() + spacing,
            option.rect.top() + 3,
            button_width,
            height
        )

        delete_rect = QRect(
            edit_rect.right() + spacing,
            option.rect.top() + 3,
            button_width,
            height
        )

        # --- Edit Button ---
        edit_button = QStyleOptionButton()
        edit_button.rect = edit_rect
        edit_button.text = "Edit"
        edit_button.state = QStyle.StateFlag.State_Enabled

        # --- Delete Button ---
        delete_button = QStyleOptionButton()
        delete_button.rect = delete_rect
        delete_button.text = "Delete"
        delete_button.state = QStyle.StateFlag.State_Enabled

        # Draw buttons
        style = option.widget.style()
        style.drawControl(QStyle.ControlElement.CE_PushButton, edit_button, painter)
        style.drawControl(QStyle.ControlElement.CE_PushButton, delete_button, painter)

    def editorEvent(self, event, model, option, index):
        """Handle mouse click events."""

        if event.type() == event.Type.MouseButtonRelease:
            if isinstance(event, QMouseEvent):
                pos = event.position().toPoint()

                button_width = 60
                spacing = 5
                height = option.rect.height() - 6

                edit_rect = QRect(
                    option.rect.left() + spacing,
                    option.rect.top() + 3,
                    button_width,
                    height
                )

                delete_rect = QRect(
                    edit_rect.right() + spacing,
                    option.rect.top() + 3,
                    button_width,
                    height
                )

                if edit_rect.contains(pos):
                    self.editClicked.emit(index.row())
                    return True

                if delete_rect.contains(pos):
                    self.deleteClicked.emit(index.row())
                    return True

        return False
