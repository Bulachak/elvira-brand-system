"""
Base Scene Class for Elvira's Brand System
"""

import os
from manim import Scene, config
from elvira_manim.config import (
    KLIMT_OBSIDIAN,
    KLIMT_ALABASTER,
    get_aspect_config,
)

class ElviraBaseScene(Scene):
    """
    Base Scene class handling aspect ratio (9:16 vs 16:9), background modes
    (dark, light, transparent), and Klimt brand styling configuration.
    """

    @property
    def aspect_ratio(self) -> str:
        return os.getenv("ELVIRA_ASPECT_RATIO", "9:16")

    @property
    def bg_mode(self) -> str:
        env_mode = os.getenv("ELVIRA_BG_MODE", "")
        if env_mode:
            return env_mode
        if config.transparent:
            return "transparent"
        return "dark"  # "dark", "light", "transparent"

    def setup(self):
        super().setup()

        # Aspect ratio frame setup
        cfg = get_aspect_config(self.aspect_ratio)
        config.pixel_width = int(cfg["pixel_width"])
        config.pixel_height = int(cfg["pixel_height"])
        config.frame_width = cfg["frame_width"]
        config.frame_height = cfg["frame_height"]

        # Background mode configuration (Dark, Light, Transparent)
        from manim import ManimColor, Rectangle

        if self.bg_mode == "transparent":
            self.camera.background_opacity = 0.0
            config.background_opacity = 0.0
        elif self.bg_mode == "light":
            self.camera.background_color = ManimColor(KLIMT_ALABASTER)
            self.camera.background_opacity = 1.0
            config.background_color = ManimColor(KLIMT_ALABASTER)
            config.background_opacity = 1.0
        else:  # "dark"
            self.camera.background_color = ManimColor(KLIMT_OBSIDIAN)
            self.camera.background_opacity = 1.0
            config.background_color = ManimColor(KLIMT_OBSIDIAN)
            config.background_opacity = 1.0

        self.camera.init_background()
        self.camera.reset()

        # Add a physical full-screen background rectangle to guarantee solid fill
        if not self.is_transparent:
            bg_col = KLIMT_ALABASTER if self.is_light else KLIMT_OBSIDIAN
            self.full_screen_bg = Rectangle(
                width=config.frame_width * 2.0,
                height=config.frame_height * 2.0,
                fill_color=bg_col,
                fill_opacity=1.0,
                stroke_width=0,
            )
            self.full_screen_bg.set_z_index(-1000)
            self.add(self.full_screen_bg)

    @property
    def is_vertical(self) -> bool:
        return self.aspect_ratio == "9:16"

    @property
    def is_transparent(self) -> bool:
        return self.bg_mode == "transparent"

    @property
    def is_light(self) -> bool:
        return self.bg_mode == "light"
