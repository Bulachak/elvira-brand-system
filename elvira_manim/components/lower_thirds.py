"""
Streamline Lower Third Banner Mobject
"""

from manim import (
    VGroup,
    Rectangle,
    Line,
    Text,
    LEFT,
    RIGHT,
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
    FONT_MONO,
)

class StreamlineLowerThird(VGroup):
    """
    Clean dark rectangular banner trimmed with golden vector streamlines
    for introducing episode titles and core mathematical definitions.
    """

    def __init__(
        self,
        main_title: str = "MEASURE THEORY",
        subtitle: str = "EP. 05: LEBESGUE INTEGRATION",
        width: float = 12.0,
        height: float = 1.4,
        bg_mode: str = "dark",
        title_font_size: int = 26,
        sub_font_size: int = 15,
        **kwargs
    ):
        super().__init__(**kwargs)

        is_light = (bg_mode == "light")
        if is_light:
            banner_bg = "#FFFFFF"
            banner_stroke = KLIMT_OCHRE
            top_line_col = KLIMT_OCHRE
            title_col = KLIMT_OBSIDIAN
            sub_col = KLIMT_OCHRE
            opacity = 0.98
        elif bg_mode == "transparent":
            banner_bg = KLIMT_OBSIDIAN
            banner_stroke = KLIMT_GOLD
            top_line_col = KLIMT_GOLD
            title_col = KLIMT_GOLD_LIGHT
            sub_col = KLIMT_GOLD
            opacity = 0.85
        else:  # "dark"
            banner_bg = "#24201C"
            banner_stroke = KLIMT_GOLD
            top_line_col = KLIMT_GOLD
            title_col = KLIMT_GOLD_LIGHT
            sub_col = KLIMT_GOLD
            opacity = 0.95

        # Background banner
        self.banner = Rectangle(
            width=width,
            height=height,
            fill_color=banner_bg,
            fill_opacity=opacity,
            stroke_color=banner_stroke,
            stroke_width=2.5,
        )

        # Top and bottom golden streamline vectors
        half_w = width / 2.0
        half_h = height / 2.0
        self.top_line = Line(
            [-half_w, half_h, 0],
            [half_w, half_h, 0],
            color=top_line_col,
            stroke_width=4.0,
        )
        self.accent_line = Line(
            [-half_w, -half_h, 0],
            [half_w, -half_h, 0],
            color=KLIMT_CRIMSON,
            stroke_width=2.0,
        )

        # Main title (Serif)
        self.title_text = Text(
            main_title,
            font=FONT_SERIF,
            font_size=title_font_size,
            color=title_col,
        )

        # Subtitle (Monospace)
        self.sub_text = Text(
            subtitle,
            font=FONT_MONO,
            font_size=sub_font_size,
            color=sub_col,
        )

        text_group = VGroup(self.title_text, self.sub_text).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        text_group.move_to(self.banner.get_center())

        self.add(self.banner, self.top_line, self.accent_line, text_group)
