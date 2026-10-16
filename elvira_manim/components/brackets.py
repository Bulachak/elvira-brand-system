"""
Klimt Corner Brackets Mobject
"""

from manim import VGroup, Line, Dot
from elvira_manim.config import KLIMT_GOLD, KLIMT_CRIMSON

class KlimtCornerBrackets(VGroup):
    """
    Custom golden corner brackets accented with jewel-like crimson dots.
    Calculates exact corner positions for non-square rectangles.
    """

    def __init__(
        self,
        width: float = 6.0,
        height: float = 3.0,
        arm_len: float = 0.35,
        stroke_width: float = 3.0,
        color: str = KLIMT_GOLD,
        accent: str = KLIMT_CRIMSON,
        **kwargs
    ):
        super().__init__(**kwargs)
        half_w, half_h = width / 2.0, height / 2.0

        def make_corner(x, y, dx, dy):
            return VGroup(
                Line([x, y, 0], [x + dx * arm_len, y, 0], stroke_width=stroke_width, color=color),
                Line([x, y, 0], [x, y + dy * arm_len, 0], stroke_width=stroke_width, color=color),
                Dot(point=[x + dx * 0.1, y + dy * 0.1, 0], radius=0.05, color=accent),
            )

        top_left = make_corner(-half_w, half_h, 1, -1)
        top_right = make_corner(half_w, half_h, -1, -1)
        bottom_right = make_corner(half_w, -half_h, -1, 1)
        bottom_left = make_corner(-half_w, -half_h, 1, 1)

        self.add(top_left, top_right, bottom_right, bottom_left)
