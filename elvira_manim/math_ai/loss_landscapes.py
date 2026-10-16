"""
Gradient Descent Path and Loss Landscape Mobject
"""

import numpy as np
from manim import VGroup, ParametricFunction, Dot, DOWN, ORIGIN
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_CRIMSON,
    KLIMT_LAPIS,
    create_math_mobject,
)

class GradientDescentPath(VGroup):
    """
    Golden optimization trajectories flowing along 2D loss landscape contours.
    """

    def __init__(
        self,
        t_range=(0, 4 * np.pi, 0.05),
        color: str = KLIMT_GOLD,
        stroke_width: float = 3.5,
        label_str: str = r"\theta_{t+1} = \theta_t - \eta \nabla_\theta \mathcal{L}(\theta)",
        **kwargs
    ):
        super().__init__(**kwargs)

        # Spiral gradient trajectory curve
        def spiral_func(t):
            r = 3.0 * np.exp(-0.25 * t)
            x = r * np.cos(t)
            y = r * np.sin(t)
            return np.array([x, y, 0])

        self.path = ParametricFunction(
            spiral_func,
            t_range=t_range,
            color=color,
            stroke_width=stroke_width,
        )
        self.add(self.path)

        # Start and end dots
        start_pt = spiral_func(t_range[0])
        end_pt = spiral_func(t_range[1])

        self.start_dot = Dot(start_pt, color=KLIMT_CRIMSON, radius=0.12)
        self.end_dot = Dot(end_pt, color=KLIMT_LAPIS, radius=0.12)
        self.add(self.start_dot, self.end_dot)

        if label_str:
            self.label = create_math_mobject(label_str, color=KLIMT_GOLD_LIGHT, font_size=24)
            self.label.next_to(self.path, DOWN, buff=0.4)
            self.add(self.label)
