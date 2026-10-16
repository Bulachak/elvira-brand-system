"""
Demonstration Scenes for Elvira's Brand System
"""

from manim import Create, FadeIn, Write, UP, DOWN, config
from elvira_manim.scenes.base import ElviraBaseScene
from elvira_manim.components import (
    TheoremCardOverlay,
    StreamlineLowerThird,
    DiscreteTileBadge,
    AudioNodePulse,
)
from elvira_manim.math_ai import (
    LebesgueIntervalMobject,
    MatrixTileGrid,
    IsoDensityContours,
    GradientDescentPath,
)

class MeasureTheoryOverlayScene(ElviraBaseScene):
    """
    Measure Theory lesson scene featuring TheoremCardOverlay,
    LebesgueIntervalMobject, and DiscreteTileBadge.
    Supports 3 background options: dark, light, and transparent.
    """

    def construct(self):
        # Top concept badge
        badge = DiscreteTileBadge(
            tag_text="[ REAL AI : MEASURE THEORY ]",
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        # Theorem card overlay
        w = 7.8 if self.is_vertical else 12.8
        h = 4.8 if self.is_vertical else 5.0
        card = TheoremCardOverlay(
            title_str="COUNTABLE ADDITIVITY AXIOM",
            latex_str=r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
            width=w,
            height=h,
            bg_mode=self.bg_mode,
            font_size=46 if self.is_vertical else 56,
            title_font_size=24 if self.is_vertical else 28,
        )
        card.next_to(badge, DOWN, buff=0.45 if self.is_vertical else 0.38)

        # Lebesgue interval number line
        interval = LebesgueIntervalMobject(
            length=w * 0.92,
            bg_mode=self.bg_mode,
            font_size=16 if self.is_vertical else 19,
        )
        interval.next_to(card, DOWN, buff=0.5 if self.is_vertical else 0.42)

        # Animation sequence
        self.play(FadeIn(badge, shift=DOWN), run_time=1.0)
        self.play(FadeIn(card, scale=1.03), run_time=1.5)
        self.play(Create(interval), run_time=2.0)
        self.wait(2)


class MatrixTransformerScene(ElviraBaseScene):
    """
    Matrix & Vision Transformer tile scene featuring MatrixTileGrid
    and StreamlineLowerThird.
    """

    def construct(self):
        lower_third = StreamlineLowerThird(
            main_title="DISCRETE MATRIX TILES",
            subtitle="WEIGHT TENSORS W ∈ ℝ^(m × n) AND PATCH EMBEDDINGS",
            width=6.8 if self.is_vertical else 7.5,
        )
        lower_third.to_edge(UP, buff=0.8)

        grid = MatrixTileGrid(rows=4, cols=4, tile_size=0.55)
        grid.next_to(lower_third, DOWN, buff=0.8)

        self.play(FadeIn(lower_third, shift=DOWN), run_time=1.0)
        self.play(Create(grid.tiles, lag_ratio=0.08), Write(grid.label), run_time=2.5)
        self.wait(2)


class GradientDescentLandscapeScene(ElviraBaseScene):
    """
    Gradient Descent optimization scene featuring IsoDensityContours
    and GradientDescentPath.
    """

    def construct(self):
        badge = DiscreteTileBadge(
            tag_text="[ LATENT LOSS LANDSCAPE ]",
            bg_mode=self.bg_mode,
        )
        badge.to_edge(UP, buff=0.8)

        contours = IsoDensityContours(num_contours=4)
        path = GradientDescentPath()

        path.move_to(contours.get_center())
        badge.next_to(contours, UP, buff=0.5)

        self.play(FadeIn(badge), Create(contours.contours), run_time=1.5)
        self.play(Create(path.path), FadeIn(path.start_dot), FadeIn(path.end_dot), Write(path.label), run_time=3.0)
        self.wait(2)
