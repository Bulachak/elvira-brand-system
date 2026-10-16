"""
Function Plot, Coordinate Axes, and Bar Chart Mobjects for Elvira Brand System
Enables graphing mathematical functions, curves, and discrete probability distributions.
"""

import numpy as np
from manim import (
    VGroup,
    Axes,
    BarChart,
    Text,
    UP,
    DOWN,
    ORIGIN,
    Line,
    Polygon,
)
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_OCHRE,
    KLIMT_LAPIS,
    KLIMT_CRIMSON,
    KLIMT_EMERALD,
    KLIMT_OBSIDIAN,
    KLIMT_ALABASTER,
    FONT_SERIF,
    FONT_MONO,
    create_math_mobject,
)


class FunctionPlotMobject(VGroup):
    """
    Coordinate axes and function curve plot styled with the Klimt palette.
    Supports Gaussian bell curve, Sigmoid, ReLU, and arbitrary mathematical functions f(x),
    with optional shaded area under the curve.
    """

    def __init__(
        self,
        func_type: str = "gaussian",  # "gaussian", "sigmoid", "relu", "quadratic"
        x_range=(-3, 3, 1),
        y_range=(0, 1.2, 0.5),
        width: float = 6.0,
        height: float = 3.2,
        bg_mode: str = "dark",
        fill_area: bool = True,
        label_str: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)

        is_light = (bg_mode == "light")
        axis_color = KLIMT_OCHRE if is_light else KLIMT_GOLD
        curve_color = KLIMT_LAPIS if is_light else KLIMT_GOLD
        label_color = KLIMT_OBSIDIAN if is_light else KLIMT_GOLD_LIGHT
        area_color = KLIMT_LAPIS if is_light else KLIMT_OCHRE

        self.axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=width,
            y_length=height,
            axis_config={
                "color": axis_color,
                "stroke_width": 2.0,
                "include_ticks": True,
                "tick_size": 0.08,
            },
            tips=True,
        )
        self.add(self.axes)

        # Select function
        if func_type == "gaussian":
            f = lambda x: np.exp(-0.5 * (x ** 2))
            default_label = r"f(x) = \frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}x^2}"
        elif func_type == "sigmoid":
            f = lambda x: 1.0 / (1.0 + np.exp(-x))
            default_label = r"\sigma(x) = \frac{1}{1 + e^{-x}}"
        elif func_type == "relu":
            f = lambda x: np.maximum(0.0, x)
            default_label = r"\text{ReLU}(x) = \max(0, x)"
        elif func_type == "quadratic":
            f = lambda x: 0.12 * (x ** 2)
            default_label = r"\mathcal{L}(\theta) = \frac{1}{2}\theta^2"
        else:
            f = lambda x: np.exp(-0.5 * (x ** 2))
            default_label = r"f(x)"

        self.curve = self.axes.plot(f, color=curve_color, stroke_width=3.5)
        self.add(self.curve)

        # Area under the curve
        if fill_area:
            self.area = self.axes.get_area(self.curve, x_range=[x_range[0], x_range[1]], color=area_color, opacity=0.35)
            self.add(self.area)
        else:
            self.area = VGroup()

        lbl_text = label_str if label_str else default_label
        self.label = create_math_mobject(lbl_text, color=label_color, font_size=24)
        self.label.next_to(self.axes, DOWN, buff=0.35)
        self.add(self.label)


class BarChartMobject(VGroup):
    """
    Discrete probability distribution bar chart using Klimt mosaic colors.
    Used for token probabilities, softmax output distributions, and discrete PMFs.
    """

    def __init__(
        self,
        values=(0.15, 0.45, 0.25, 0.85, 0.35),
        bar_names=("z_1", "z_2", "z_3", "z_4", "z_5"),
        width: float = 6.0,
        height: float = 3.0,
        bg_mode: str = "dark",
        label_str: str = r"P(Z = z_i) \sim \text{Softmax}(W \cdot x)",
        **kwargs
    ):
        super().__init__(**kwargs)

        is_light = (bg_mode == "light")
        axis_color = KLIMT_OCHRE if is_light else KLIMT_GOLD
        label_color = KLIMT_OBSIDIAN if is_light else KLIMT_GOLD_LIGHT

        colors = [KLIMT_LAPIS, KLIMT_GOLD, KLIMT_CRIMSON, KLIMT_EMERALD, KLIMT_OCHRE]

        values_list = list(values)
        names_list = list(bar_names) if bar_names else None

        sub_map = {"_0": "₀", "_1": "₁", "_2": "₂", "_3": "₃", "_4": "₄", "_5": "₅"}
        clean_names = []
        if names_list:
            for name in names_list:
                n = str(name)
                for k, v in sub_map.items():
                    n = n.replace(k, v)
                clean_names.append(n)
        else:
            clean_names = None

        self.chart = BarChart(
            values=values_list,
            bar_names=clean_names,
            y_range=[0, 1.0, 0.25],
            x_length=width,
            y_length=height,
            bar_colors=colors[:len(values_list)],
            bar_width=0.45,
            x_axis_config={
                "color": axis_color,
                "stroke_width": 2.0,
                "label_constructor": Text,
                "font_size": 20,
            },
            y_axis_config={
                "color": axis_color,
                "stroke_width": 2.0,
                "label_constructor": Text,
                "font_size": 18,
            },
        )
        self.add(self.chart)

        if label_str:
            self.label = create_math_mobject(label_str, color=label_color, font_size=24)
            self.label.next_to(self.chart, DOWN, buff=0.35)
            self.add(self.label)


class TextNodeCard(VGroup):
    """
    High-contrast editorial text card for conceptual definitions,
    theorems, quotes, or multi-line educational breakdowns.
    """

    def __init__(
        self,
        title_str: str = "MEASURABLE SPACE DEFINITION",
        body_text: str = "A pair (X, Σ) where X is a set and Σ is a σ-algebra of subsets of X. Every element of Σ is called a measurable set.",
        width: float = 12.0,
        height: float = 4.8,
        bg_mode: str = "dark",
        title_size: int | None = None,
        body_size: int | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        from manim import RoundedRectangle
        from elvira_manim.components.brackets import KlimtCornerBrackets

        is_light = (bg_mode == "light")
        bg_color = "#FFFFFF" if is_light else ("#1A1815" if bg_mode == "transparent" else "#24201C")
        stroke_color = KLIMT_OCHRE if is_light else KLIMT_GOLD
        text_color = KLIMT_OBSIDIAN if is_light else KLIMT_GOLD_LIGHT
        title_color = KLIMT_OCHRE if is_light else KLIMT_GOLD
        opacity = 0.98 if is_light else (0.85 if bg_mode == "transparent" else 0.96)

        t_size = title_size if title_size else (28 if width > 9.0 else 22)
        b_size = body_size if body_size else (24 if width > 9.0 else 18)
        wrap_chars = 56 if width > 9.0 else 38

        self.card_bg = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            fill_color=bg_color,
            fill_opacity=opacity,
            stroke_color=stroke_color,
            stroke_width=2.8,
        )

        self.corners = KlimtCornerBrackets(
            width=width,
            height=height,
            arm_len=0.5 if width > 9.0 else 0.4,
            stroke_width=2.8,
            color=stroke_color,
            accent=KLIMT_CRIMSON,
        )

        self.title = Text(
            title_str,
            font=FONT_SERIF,
            font_size=t_size,
            color=title_color,
        )
        if self.title.width > width * 0.88:
            self.title.scale_to_fit_width(width * 0.88)
        self.title.next_to(self.card_bg.get_top(), DOWN, buff=0.35)

        # Word-wrapped body text
        wrapped_body = body_text
        if "\n" not in body_text and len(body_text) > wrap_chars:
            import textwrap
            wrapped_body = textwrap.fill(body_text, width=wrap_chars)

        self.body = Text(
            wrapped_body,
            font=FONT_SERIF,
            font_size=b_size,
            color=text_color,
            line_spacing=0.9,
        )
        if self.body.width > width * 0.88:
            self.body.scale_to_fit_width(width * 0.88)
        self.body.next_to(self.title, DOWN, buff=0.4)

        self.add(self.card_bg, self.corners, self.title, self.body)
