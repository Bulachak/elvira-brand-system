"""
Discrete Tile Badge Mobject
"""

from manim import VGroup, RoundedRectangle, Text, ORIGIN
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_OBSIDIAN,
    KLIMT_GOLD_LIGHT,
    KLIMT_ALABASTER,
    KLIMT_OCHRE,
    FONT_SERIF,
)

class DiscreteTileBadge(VGroup):
    """
    Semi-translucent rectilinear mosaic badges for tagging mathematical
    frameworks, chapter markers, or topic tags.
    Supports dark, light, and transparent background modes.
    """

    def __init__(
        self,
        tag_text: str = "[ REAL AI: MEASURE THEORY ]",
        font_size: int = 16,
        padding_x: float = 0.35,
        padding_y: float = 0.2,
        bg_mode: str = "dark",
        **kwargs
    ):
        super().__init__(**kwargs)

        if bg_mode == "light":
            bg_color = "#FFFFFF"
            stroke_color = KLIMT_OCHRE
            text_color = KLIMT_OBSIDIAN
        elif bg_mode == "transparent":
            bg_color = KLIMT_OBSIDIAN
            stroke_color = KLIMT_GOLD
            text_color = KLIMT_GOLD_LIGHT
        else:  # "dark"
            bg_color = "#24201C"
            stroke_color = KLIMT_GOLD
            text_color = KLIMT_GOLD_LIGHT

        self.label = Text(
            tag_text,
            font=FONT_SERIF,
            font_size=font_size,
            color=text_color,
        )

        width = self.label.width + padding_x * 2.0
        height = self.label.height + padding_y * 2.0

        self.badge_bg = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            fill_color=bg_color,
            fill_opacity=0.88,
            stroke_color=stroke_color,
            stroke_width=2.0,
        )

        self.label.move_to(self.badge_bg.get_center())
        self.add(self.badge_bg, self.label)
