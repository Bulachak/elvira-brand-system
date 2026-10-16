"""
Iso-density Contours and Probability Density Mobject
"""

import numpy as np
from manim import VGroup, Ellipse, DOWN, ORIGIN
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_LAPIS,
    KLIMT_EMERALD,
    KLIMT_CRIMSON,
    create_math_mobject,
)

class IsoDensityContours(VGroup):
    """
    Concentric elliptical ring Mobjects representing continuous probability density
    contours p(x), Radial Basis Functions, and Mixture of Experts latent spheres.
    """

    def __init__(
        self,
        num_contours: int = 4,
        base_width: float = 1.2,
        base_height: float = 0.8,
        scale_factor: float = 1.4,
        label_str: str = r"p(x \mid \mu, \Sigma)",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.contours = VGroup()
        colors = [KLIMT_CRIMSON, KLIMT_GOLD, KLIMT_EMERALD, KLIMT_LAPIS]

        for i in range(num_contours):
            w = base_width * (scale_factor ** i)
            h = base_height * (scale_factor ** i)
            col = colors[i % len(colors)]
            contour = Ellipse(
                width=w,
                height=h,
                color=col,
                stroke_width=2.5,
                stroke_opacity=1.0 - (i * 0.18),
                fill_color=col,
                fill_opacity=0.1,
            )
            self.contours.add(contour)

        self.add(self.contours)

        if label_str:
            self.label = create_math_mobject(label_str, color=KLIMT_GOLD_LIGHT, font_size=26)
            self.label.next_to(self.contours, DOWN, buff=0.3)
            self.add(self.label)
