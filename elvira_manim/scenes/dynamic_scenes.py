"""
Dynamic Configurable Scene for Elvira's Brand System
Enables arbitrary LaTeX formulas, text cards, function plots, bar charts,
and custom Manim visualizer code via ELVIRA_SCENE_CONFIG.
"""

import os
import json
import numpy as np
from manim import (
    Create,
    FadeIn,
    Write,
    UP,
    DOWN,
    ORIGIN,
    config,
    VGroup,
    Axes,
    BarChart,
    Text,
    Circle,
    Line,
    Dot,
    Arrow,
    Square,
    Rectangle,
)
from elvira_manim.scenes.base import ElviraBaseScene
from elvira_manim.components import (
    TheoremCardOverlay,
    StreamlineLowerThird,
    DiscreteTileBadge,
    AudioNodePulse,
    KlimtCornerBrackets,
)
from elvira_manim.math_ai import (
    LebesgueIntervalMobject,
    MatrixTileGrid,
    IsoDensityContours,
    GradientDescentPath,
    FunctionPlotMobject,
    BarChartMobject,
    TextNodeCard,
)
from elvira_manim.config import (
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_OCHRE,
    KLIMT_CRIMSON,
    KLIMT_LAPIS,
    KLIMT_EMERALD,
    KLIMT_OBSIDIAN,
    KLIMT_ALABASTER,
    FONT_SERIF,
    FONT_SANS,
    FONT_MONO,
    create_math_mobject,
)


class ElviraDynamicStudioScene(ElviraBaseScene):
    """
    Dynamically constructs a brand-accurate mathematical animation based on
    parameters passed through the ELVIRA_SCENE_CONFIG environment variable.
    """

    def get_studio_config(self) -> dict:
        raw = os.environ.get("ELVIRA_SCENE_CONFIG", "")
        if raw:
            try:
                if os.path.exists(raw):
                    with open(raw, "r", encoding="utf-8") as f:
                        return json.load(f)
                return json.loads(raw)
            except Exception as e:
                print(f"[ELVIRA DYNAMIC SCENE] Warning: Failed to parse ELVIRA_SCENE_CONFIG: {e}")
        return {
            "scene_type": "theorem_card",
            "badge_text": "[ REAL AI // MEASURE THEORY ]",
            "title": "COUNTABLE ADDITIVITY AXIOM",
            "subtitle": "LEBESGUE MEASURE SPACE (X, Σ, μ)",
            "latex_formula": r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
            "show_interval": True,
        }

    def construct(self):
        cfg = self.get_studio_config()
        scene_type = cfg.get("scene_type", "theorem_card")
        badge_text = cfg.get("badge_text", "[ REAL AI // MATHEMATICAL FOUNDATION ]")
        title = cfg.get("title", "APPLIED MATHEMATICS")
        subtitle = cfg.get("subtitle", "MACHINE LEARNING FRAMEWORK")
        formula = cfg.get("latex_formula", r"\mathbf{W} \cdot \mathbf{x} + \mathbf{b}")
        body_text = cfg.get("body_text", "A measurable space is a pair (X, Σ) where Σ is a σ-algebra over X.")

        # Scale parameters according to aspect ratio
        w_card = 7.8 if self.is_vertical else 12.8
        h_card = 4.8 if self.is_vertical else 4.7

        if scene_type == "theorem_card":
            self._construct_theorem_card(badge_text, title, formula, w_card, h_card, cfg)
        elif scene_type == "text_card":
            self._construct_text_card(badge_text, title, body_text, w_card, h_card, cfg)
        elif scene_type == "function_plot":
            self._construct_function_plot(badge_text, title, formula, w_card, cfg)
        elif scene_type == "bar_chart":
            self._construct_bar_chart(badge_text, title, formula, w_card, cfg)
        elif scene_type == "lebesgue_interval":
            self._construct_lebesgue_interval(badge_text, title, formula, w_card, cfg)
        elif scene_type == "matrix_grid":
            self._construct_matrix_grid(badge_text, title, subtitle, w_card, cfg)
        elif scene_type == "iso_density":
            self._construct_iso_density(badge_text, title, formula, w_card, cfg)
        elif scene_type == "gradient_descent":
            self._construct_gradient_descent(badge_text, title, formula, w_card, cfg)
        elif scene_type == "custom_code":
            self._construct_custom_code(cfg)
        else:
            self._construct_pure_formula(badge_text, title, formula, w_card, cfg)

    def _construct_theorem_card(self, badge_text, title, formula, w_card, h_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=0.85 if self.is_vertical else 0.35)

        card = TheoremCardOverlay(
            title_str=title,
            latex_str=formula,
            width=w_card,
            height=h_card,
            bg_mode=self.bg_mode,
            font_size=46 if self.is_vertical else 56,
            title_font_size=24 if self.is_vertical else 28,
            arm_len=0.45 if self.is_vertical else 0.55,
        )
        card.next_to(badge, DOWN, buff=0.35 if self.is_vertical else 0.30)

        self.play(FadeIn(badge, shift=DOWN), run_time=0.8)
        self.play(FadeIn(card, scale=1.02), run_time=1.4)

        if cfg.get("show_interval", True):
            interval = LebesgueIntervalMobject(
                length=w_card * 0.92,
                bg_mode=self.bg_mode,
                font_size=16 if self.is_vertical else 19,
            )
            interval.next_to(card, DOWN, buff=0.40 if self.is_vertical else 0.32)
            self.play(Create(interval), run_time=1.8)
            self.wait(2)
        else:
            self.wait(3)

    def _construct_text_card(self, badge_text, title, body_text, w_card, h_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        card = TextNodeCard(
            title_str=title,
            body_text=body_text,
            width=w_card,
            height=h_card * 1.05,
            bg_mode=self.bg_mode,
        )
        card.next_to(badge, DOWN, buff=0.45 if self.is_vertical else 0.4)

        self.play(FadeIn(badge, shift=DOWN), run_time=0.8)
        self.play(FadeIn(card, scale=1.02), run_time=1.4)
        self.wait(3.0)

    def _construct_function_plot(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        func_type = cfg.get("func_type", "gaussian")
        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle="CONTINUOUS MATHEMATICAL FUNCTION f(x)",
            width=w_card,
            bg_mode=self.bg_mode,
        )
        lower_third.next_to(badge, DOWN, buff=0.35)

        plot = FunctionPlotMobject(
            func_type=func_type,
            width=w_card * 0.95,
            height=4.0 if self.is_vertical else 4.6,
            bg_mode=self.bg_mode,
            label_str=formula,
        )
        plot.next_to(lower_third, DOWN, buff=0.5 if self.is_vertical else 0.42)

        self.play(FadeIn(badge), FadeIn(lower_third), run_time=0.9)
        self.play(Create(plot.axes), run_time=1.2)
        self.play(Create(plot.curve), FadeIn(plot.area), run_time=1.8)
        self.play(Write(plot.label), run_time=1.0)
        self.wait(2.5)

    def _construct_bar_chart(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle="DISCRETE PROBABILITY DISTRIBUTION P(X = x)",
            width=w_card,
            bg_mode=self.bg_mode,
        )
        lower_third.next_to(badge, DOWN, buff=0.35)

        chart = BarChartMobject(
            width=w_card * 0.95,
            height=3.8 if self.is_vertical else 4.6,
            bg_mode=self.bg_mode,
            label_str=formula,
        )
        chart.next_to(lower_third, DOWN, buff=0.5 if self.is_vertical else 0.42)

        self.play(FadeIn(badge), FadeIn(lower_third), run_time=0.9)
        self.play(Create(chart.chart), run_time=2.0)
        self.play(Write(chart.label), run_time=1.0)
        self.wait(2.5)

    def _construct_lebesgue_interval(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle="PARTITIONING CONTINUOUS MEASURE SPACE [0, 1]",
            width=w_card,
            bg_mode=self.bg_mode,
        )
        lower_third.next_to(badge, DOWN, buff=0.35)

        interval = LebesgueIntervalMobject(
            length=w_card * 0.92,
            bg_mode=self.bg_mode,
            font_size=16 if self.is_vertical else 20,
        )
        interval.next_to(lower_third, DOWN, buff=0.5 if self.is_vertical else 0.45)

        formula_color = KLIMT_OBSIDIAN if self.bg_mode == "light" else KLIMT_GOLD_LIGHT
        formula_mob = create_math_mobject(
            formula,
            font_size=42 if self.is_vertical else 52,
            color=formula_color,
            max_width=w_card * 0.88,
        )
        formula_mob.next_to(interval, DOWN, buff=0.5 if self.is_vertical else 0.42)

        self.play(FadeIn(badge, shift=DOWN), run_time=0.8)
        self.play(FadeIn(lower_third, shift=DOWN), run_time=1.0)
        self.play(Create(interval), run_time=1.8)
        self.play(Write(formula_mob), run_time=1.4)
        self.wait(2.5)

    def _construct_matrix_grid(self, badge_text, title, subtitle, w_card, cfg):
        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle=subtitle,
            width=w_card,
        )
        lower_third.to_edge(UP, buff=0.8 if self.is_vertical else 0.5)

        rows = int(cfg.get("matrix_rows", 4))
        cols = int(cfg.get("matrix_cols", 4))
        tile_size = 0.55 if self.is_vertical else 0.65
        grid = MatrixTileGrid(rows=rows, cols=cols, tile_size=tile_size)
        grid.next_to(lower_third, DOWN, buff=0.6)

        self.play(FadeIn(lower_third, shift=DOWN), run_time=0.9)
        self.play(Create(grid.tiles, lag_ratio=0.06), Write(grid.label), run_time=2.4)
        self.wait(2.5)

    def _construct_iso_density(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle="CONTINUOUS PROBABILITY FIELD p(x) & GAUSSIAN SPHERES",
            width=w_card,
            bg_mode=self.bg_mode,
        )
        lower_third.next_to(badge, DOWN, buff=0.35)

        num_contours = int(cfg.get("num_contours", 4))
        contours = IsoDensityContours(num_contours=num_contours)
        contours.next_to(lower_third, DOWN, buff=0.5)

        formula_color = KLIMT_OBSIDIAN if self.bg_mode == "light" else KLIMT_GOLD_LIGHT
        formula_mob = create_math_mobject(
            formula,
            font_size=36 if self.is_vertical else 46,
            color=formula_color,
            max_width=w_card * 0.88,
        )
        formula_mob.next_to(contours, DOWN, buff=0.45)

        self.play(FadeIn(badge), FadeIn(lower_third), run_time=1.0)
        self.play(Create(contours.contours, lag_ratio=0.15), run_time=2.2)
        self.play(Write(formula_mob), run_time=1.2)
        self.wait(2.5)

    def _construct_gradient_descent(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.45)

        lower_third = StreamlineLowerThird(
            main_title=title,
            subtitle="OPTIMIZATION LOSS LANDSCAPE ∇L(θ)",
            width=w_card,
            bg_mode=self.bg_mode,
        )
        lower_third.next_to(badge, DOWN, buff=0.35)

        contours = IsoDensityContours(num_contours=4)
        path = GradientDescentPath()
        path.move_to(contours.get_center())

        group = VGroup(contours, path)
        group.next_to(lower_third, DOWN, buff=0.5)

        formula_color = KLIMT_OBSIDIAN if self.bg_mode == "light" else KLIMT_GOLD_LIGHT
        formula_mob = create_math_mobject(
            formula,
            font_size=36 if self.is_vertical else 46,
            color=formula_color,
            max_width=w_card * 0.88,
        )
        formula_mob.next_to(group, DOWN, buff=0.45)

        self.play(FadeIn(badge), FadeIn(lower_third), run_time=0.9)
        self.play(Create(contours.contours), run_time=1.8)
        self.play(Create(path.path), FadeIn(path.start_dot), FadeIn(path.end_dot), Write(path.label), run_time=2.4)
        self.play(Write(formula_mob), run_time=1.2)
        self.wait(2.5)

    def _construct_pure_formula(self, badge_text, title, formula, w_card, cfg):
        badge = DiscreteTileBadge(
            tag_text=badge_text,
            bg_mode=self.bg_mode,
            font_size=18 if self.is_vertical else 20,
        )
        badge.to_edge(UP, buff=1.0 if self.is_vertical else 0.5)

        card = TheoremCardOverlay(
            title_str=title,
            latex_str=formula,
            width=w_card,
            height=5.2 if self.is_vertical else 5.4,
            bg_mode=self.bg_mode,
            font_size=48 if self.is_vertical else 60,
            title_font_size=24 if self.is_vertical else 28,
            arm_len=0.45 if self.is_vertical else 0.55,
        )
        card.next_to(badge, DOWN, buff=0.5 if self.is_vertical else 0.4)

        self.play(FadeIn(badge, shift=DOWN), run_time=0.8)
        self.play(FadeIn(card, scale=1.03), run_time=1.5)
        self.wait(3.0)

    def _construct_custom_code(self, cfg):
        code_str = cfg.get("custom_code", "")
        if not code_str:
            self._construct_pure_formula(
                cfg.get("badge_text", "[ REAL AI ]"),
                cfg.get("title", "CUSTOM MATHEMATICS"),
                cfg.get("latex_formula", r"f(x) = \int e^{-x} dx"),
                6.8,
                cfg
            )
            return

        local_vars = {
            "self": self,
            "config": config,
            "KLIMT_GOLD": KLIMT_GOLD,
            "KLIMT_GOLD_LIGHT": KLIMT_GOLD_LIGHT,
            "KLIMT_OCHRE": KLIMT_OCHRE,
            "KLIMT_LAPIS": KLIMT_LAPIS,
            "KLIMT_CRIMSON": KLIMT_CRIMSON,
            "KLIMT_EMERALD": KLIMT_EMERALD,
            "KLIMT_OBSIDIAN": KLIMT_OBSIDIAN,
            "KLIMT_ALABASTER": KLIMT_ALABASTER,
            "FunctionPlotMobject": FunctionPlotMobject,
            "BarChartMobject": BarChartMobject,
            "TextNodeCard": TextNodeCard,
            "TheoremCardOverlay": TheoremCardOverlay,
            "StreamlineLowerThird": StreamlineLowerThird,
            "DiscreteTileBadge": DiscreteTileBadge,
            "MatrixTileGrid": MatrixTileGrid,
            "LebesgueIntervalMobject": LebesgueIntervalMobject,
            "IsoDensityContours": IsoDensityContours,
            "GradientDescentPath": GradientDescentPath,
            "create_math_mobject": create_math_mobject,
        }
        try:
            exec(code_str, globals(), local_vars)
        except Exception as e:
            print(f"[ELVIRA DYNAMIC SCENE] Error executing custom code: {e}")
            err_text = Text(f"Code Error: {e}", font=FONT_SERIF, font_size=18, color=KLIMT_CRIMSON)
            self.play(FadeIn(err_text))
            self.wait(2)
