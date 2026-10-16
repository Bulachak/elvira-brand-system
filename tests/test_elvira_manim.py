"""
Unit Tests for Elvira Brand System Manim Library
"""

import unittest
from elvira_manim.config import (
    KLIMT_PALETTE,
    KLIMT_GOLD,
    get_aspect_config,
)
from elvira_manim.components import (
    KlimtCornerBrackets,
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
from elvira_manim.scenes import (
    MeasureTheoryOverlayScene,
    MatrixTransformerScene,
    GradientDescentLandscapeScene,
    ElviraDynamicStudioScene,
)
from render_cli import build_manim_cmd

class TestElviraManim(unittest.TestCase):

    def test_palette_integrity(self):
        self.assertIn("Gold", KLIMT_PALETTE)
        self.assertEqual(KLIMT_PALETTE["Gold"], "#D4AF37")
        self.assertEqual(KLIMT_GOLD, "#D4AF37")

    def test_aspect_config(self):
        cfg_v = get_aspect_config("9:16")
        self.assertEqual(cfg_v["pixel_width"], 1080)
        self.assertEqual(cfg_v["pixel_height"], 1920)

        cfg_h = get_aspect_config("16:9")
        self.assertEqual(cfg_h["pixel_width"], 1920)
        self.assertEqual(cfg_h["pixel_height"], 1080)

    def test_components_instantiation(self):
        brackets = KlimtCornerBrackets(width=5.0, height=3.0)
        self.assertIsNotNone(brackets)

        card = TheoremCardOverlay(title_str="TEST AXIOM")
        self.assertIsNotNone(card)

        lower_third = StreamlineLowerThird(main_title="TEST TITLE")
        self.assertIsNotNone(lower_third)

        badge = DiscreteTileBadge(tag_text="[ TEST ]")
        self.assertIsNotNone(badge)

        pulse = AudioNodePulse(num_rings=3)
        self.assertIsNotNone(pulse)

    def test_math_ai_mobjects(self):
        interval = LebesgueIntervalMobject()
        self.assertIsNotNone(interval)

        grid = MatrixTileGrid(rows=3, cols=3)
        self.assertIsNotNone(grid)

        contours = IsoDensityContours(num_contours=3)
        self.assertIsNotNone(contours)

        path = GradientDescentPath()
        self.assertIsNotNone(path)

        from elvira_manim.math_ai import FunctionPlotMobject, BarChartMobject, TextNodeCard
        plot = FunctionPlotMobject(func_type="gaussian", bg_mode="light")
        self.assertIsNotNone(plot)

        chart = BarChartMobject(values=[0.2, 0.4, 0.8], bar_names=["A", "B", "C"])
        self.assertIsNotNone(chart)

        card = TextNodeCard(title_str="TEST TITLE", body_text="Testing multi-line text node card")
        self.assertIsNotNone(card)

    def test_scene_classes(self):
        scene_1 = MeasureTheoryOverlayScene()
        self.assertTrue(scene_1.is_vertical)

        scene_2 = MatrixTransformerScene()
        self.assertIsNotNone(scene_2)

        scene_3 = GradientDescentLandscapeScene()
        self.assertIsNotNone(scene_3)

        scene_4 = ElviraDynamicStudioScene()
        self.assertIsNotNone(scene_4)

    def test_render_cli_cmd(self):
        cmd = build_manim_cmd(
            scene_name="MeasureTheoryOverlayScene",
            aspect_ratio="9:16",
            quality="medium",
            transparent=True,
        )
        self.assertIn("MeasureTheoryOverlayScene", cmd)
        self.assertIn("-t", cmd)
        self.assertIn("1080,1920", cmd)

if __name__ == "__main__":
    unittest.main()
