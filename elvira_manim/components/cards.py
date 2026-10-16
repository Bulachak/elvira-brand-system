"""
Theorem Card Overlay Mobject
"""

from manim import (
    VGroup,
    RoundedRectangle,
    Text,
    UP,
    DOWN,
    ORIGIN,
)
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_OBSIDIAN,
    KLIMT_ALABASTER,
    KLIMT_CRIMSON,
    KLIMT_OCHRE,
    FONT_SERIF,
    create_math_mobject,
)
from elvira_manim.components.brackets import KlimtCornerBrackets

class TheoremCardOverlay(VGroup):
    """
    High-contrast card container styled with Klimt gold borders and corner brackets.
    Supports 3 background choices: dark, light, and transparent overlay modes.
    """

    def __init__(
        self,
        latex_str: str = r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
        title_str: str = "COUNTABLE ADDITIVITY AXIOM",
        width: float = 12.0,
        height: float = 4.8,
        bg_mode: str = "dark",  # "dark", "light", or "transparent"
        font_size: int = 52,
        title_font_size: int = 26,
        arm_len: float = 0.5,
        **kwargs
    ):
        super().__init__(**kwargs)

        if bg_mode == "light":
            bg_color = "#FFFFFF"
            bg_opacity = 0.98
            stroke_color = KLIMT_OCHRE
            text_color = KLIMT_OBSIDIAN
            title_color = KLIMT_OCHRE
        elif bg_mode == "transparent":
            bg_color = KLIMT_OBSIDIAN
            bg_opacity = 0.82
            stroke_color = KLIMT_GOLD
            text_color = KLIMT_GOLD_LIGHT
            title_color = KLIMT_GOLD
        else:  # "dark"
            bg_color = "#24201C"
            bg_opacity = 0.95
            stroke_color = KLIMT_GOLD
            text_color = KLIMT_GOLD_LIGHT
            title_color = KLIMT_GOLD

        # Main background card
        self.card_bg = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            fill_color=bg_color,
            fill_opacity=bg_opacity,
            stroke_color=stroke_color,
            stroke_width=2.8,
        )

        # Corner brackets
        self.corners = KlimtCornerBrackets(
            width=width,
            height=height,
            arm_len=arm_len,
            stroke_width=2.8,
            color=stroke_color,
            accent=KLIMT_CRIMSON,
        )

        # Title text
        self.title = Text(
            title_str,
            font=FONT_SERIF,
            font_size=title_font_size,
            color=title_color,
        )
        if self.title.width > width * 0.88:
            self.title.scale_to_fit_width(width * 0.88)

        self.title.next_to(self.card_bg.get_top(), DOWN, buff=0.35)

        # Formula math Mobject (Hero of the slide)
        self.formula = create_math_mobject(
            latex_str,
            color=text_color,
            font_size=font_size,
            max_width=width * 0.88,
        )
        self.formula.move_to(self.card_bg.get_center() + DOWN * 0.2)

        self.add(self.card_bg, self.corners, self.title, self.formula)
