"""Animate scrollbar opacity for hover fading."""

from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect


def _fade_scrollbar(self, visible: bool, duration: int = 150) -> None:
    """Fade the horizontal scrollbar in or out over *duration* milliseconds.

    The scrollbar's policy is adjusted before/after the animation to ensure
    it only takes space when visible but still allows the opacity effect to
    render the transition smoothly.
    """
    if self.scroll_area is None:
        return

    bar = self.scroll_area.horizontalScrollBar()
    if bar is None:
        return

    # ensure the scrollbar has an opacity effect
    effect = bar.graphicsEffect()
    if not isinstance(effect, QGraphicsOpacityEffect):
        effect = QGraphicsOpacityEffect(bar)
        bar.setGraphicsEffect(effect)
        # start fully transparent so showing later fades in
        effect.setOpacity(0.0)

    # when making visible, show and set policy first so layout includes it
    if visible:
        # policy belongs to the scroll area, not the bar itself
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        bar.show()

    anim = QPropertyAnimation(effect, b"opacity", bar)
    anim.setDuration(duration)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(1.0 if visible else 0.0)

    def on_finished():
        if not visible:
            # hide after fade out so it doesn't take space
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            bar.hide()
        # keep a reference around until finished
        bar._fade_anim = None

    anim.finished.connect(on_finished)
    bar._fade_anim = anim
    anim.start()
