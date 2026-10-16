"""
Lebesgue Interval and Measure Theory Mobject
"""

from manim import VGroup, NumberLine, Dot, Rectangle, Text, UP, DOWN
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_LAPIS,
    KLIMT_OCHRE,
    KLIMT_EMERALD,
    KLIMT_OBSIDIAN,
    FONT_SERIF,
)

class LebesgueIntervalMobject(VGroup):
    """
    NumberLine and interval partitioning visualization for Measure Theory lessons,
    displaying set measures and point partitions.
    """

    def __init__(
        self,
        x_range=(0, 1, 0.25),
        length: float = 11.0,
        points=(0.2, 0.5, 0.75),
        bg_mode: str = "dark",
        font_size: int = 18,
        line_color: str | None = None,
        point_color: str = KLIMT_LAPIS,
        **kwargs
    ):
        super().__init__(**kwargs)

        is_light = (bg_mode == "light")
        actual_line_color = line_color if line_color else (KLIMT_OCHRE if is_light else KLIMT_GOLD)
        label_color = KLIMT_OBSIDIAN if is_light else KLIMT_GOLD_LIGHT

        # Number line without default MathTex numbers
        self.line = NumberLine(
            x_range=x_range,
            length=length,
            color=actual_line_color,
            include_numbers=False,
            stroke_width=3.0,
        )
        self.add(self.line)

        # Number labels below tick marks
        labels = VGroup()
        start, end, step = x_range
        val = start
        while val <= end + 1e-5:
            pt = self.line.n2p(val)
            lbl = Text(f"{val:g}", font=FONT_SERIF, font_size=font_size, color=label_color)
            lbl.next_to(pt, DOWN, buff=0.22)
            labels.add(lbl)
            val += step

        self.add(labels)

        # Sample points on interval
        self.dots = VGroup(
            *[Dot(self.line.n2p(p), color=point_color, radius=0.08) for p in points]
        )
        self.add(self.dots)

        # Highlighted interval rectangle (partition measure)
        if len(points) >= 2:
            p1, p2 = points[0], points[1]
            pos1, pos2 = self.line.n2p(p1), self.line.n2p(p2)
            w = abs(pos2[0] - pos1[0])
            self.partition_rect = Rectangle(
                width=w,
                height=0.25,
                fill_color=KLIMT_EMERALD,
                fill_opacity=0.45,
                stroke_color=KLIMT_GOLD,
                stroke_width=1.5,
            )
            self.partition_rect.move_to((pos1 + pos2) / 2.0)
            self.add(self.partition_rect)
