"""
Audio Node Pulse Mobject
"""

from manim import VGroup, Circle, Dot, ORIGIN
from elvira_manim.config import KLIMT_GOLD, KLIMT_CRIMSON

class AudioNodePulse(VGroup):
    """
    Concentric golden ring vectors representing audio reactivity or node pulse focus points.
    """

    def __init__(
        self,
        num_rings: int = 3,
        base_radius: float = 0.3,
        ring_step: float = 0.25,
        color: str = KLIMT_GOLD,
        center_color: str = KLIMT_CRIMSON,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.center_dot = Dot(point=ORIGIN, radius=0.08, color=center_color)
        self.add(self.center_dot)

        self.rings = VGroup()
        for i in range(num_rings):
            r = base_radius + i * ring_step
            opacity = 1.0 - (i * 0.25)
            ring = Circle(
                radius=r,
                color=color,
                stroke_width=2.5 - (i * 0.5),
                stroke_opacity=max(0.2, opacity),
            )
            self.rings.add(ring)

        self.add(self.rings)
