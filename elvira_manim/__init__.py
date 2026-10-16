"""
Elvira Brand System Manim Package
"""

from .config import (
    KLIMT_PALETTE,
    KLIMT_GOLD,
    KLIMT_GOLD_LIGHT,
    KLIMT_OCHRE,
    KLIMT_LAPIS,
    KLIMT_CRIMSON,
    KLIMT_EMERALD,
    KLIMT_OBSIDIAN,
    KLIMT_ALABASTER,
    FONT_SERIF,
    FONT_SANS,
    FONT_MONO,
    get_aspect_config,
)

from .components import (
    KlimtCornerBrackets,
    TheoremCardOverlay,
    StreamlineLowerThird,
    DiscreteTileBadge,
    AudioNodePulse,
)

from .math_ai import (
    LebesgueIntervalMobject,
    MatrixTileGrid,
    IsoDensityContours,
    GradientDescentPath,
)

from .scenes import (
    ElviraBaseScene,
    MeasureTheoryOverlayScene,
    MatrixTransformerScene,
    GradientDescentLandscapeScene,
)

__all__ = [
    "KLIMT_PALETTE",
    "KLIMT_GOLD",
    "KLIMT_GOLD_LIGHT",
    "KLIMT_OCHRE",
    "KLIMT_LAPIS",
    "KLIMT_CRIMSON",
    "KLIMT_EMERALD",
    "KLIMT_OBSIDIAN",
    "KLIMT_ALABASTER",
    "FONT_SERIF",
    "FONT_SANS",
    "FONT_MONO",
    "get_aspect_config",
    "KlimtCornerBrackets",
    "TheoremCardOverlay",
    "StreamlineLowerThird",
    "DiscreteTileBadge",
    "AudioNodePulse",
    "LebesgueIntervalMobject",
    "MatrixTileGrid",
    "IsoDensityContours",
    "GradientDescentPath",
    "ElviraBaseScene",
    "MeasureTheoryOverlayScene",
    "MatrixTransformerScene",
    "GradientDescentLandscapeScene",
]
