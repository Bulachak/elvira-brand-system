"""
Matrix Tile Grid Mobject
"""

from manim import VGroup, Rectangle, RIGHT, DOWN, ORIGIN
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_LAPIS,
    KLIMT_CRIMSON,
    KLIMT_EMERALD,
    KLIMT_GOLD_LIGHT,
    create_math_mobject,
)

class MatrixTileGrid(VGroup):
    """
    Discrete rectilinear stacked tile grids representing weight matrices
    W in R^{m x n} and Vision Transformer patch embeddings.
    """

    def __init__(
        self,
        rows: int = 4,
        cols: int = 4,
        tile_size: float = 0.5,
        tile_spacing: float = 0.08,
        stroke_color: str = KLIMT_GOLD,
        label_str: str = r"W \in \mathbb{R}^{m \times n}",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.tiles = VGroup()
        color_cycle = [KLIMT_LAPIS, KLIMT_EMERALD, KLIMT_CRIMSON, KLIMT_GOLD]

        for r in range(rows):
            for c in range(cols):
                color_idx = (r + c) % len(color_cycle)
                tile = Rectangle(
                    width=tile_size,
                    height=tile_size,
                    fill_color=color_cycle[color_idx],
                    fill_opacity=0.6,
                    stroke_color=stroke_color,
                    stroke_width=2.0,
                )
                x = c * (tile_size + tile_spacing)
                y = -r * (tile_size + tile_spacing)
                tile.move_to([x, y, 0])
                self.tiles.add(tile)

        # Center the tile group
        self.tiles.move_to(ORIGIN)
        self.add(self.tiles)

        if label_str:
            self.label = create_math_mobject(label_str, color=KLIMT_GOLD_LIGHT, font_size=28)
            self.label.next_to(self.tiles, DOWN, buff=0.3)
            self.add(self.label)
