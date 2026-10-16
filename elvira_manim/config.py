"""
Brand Configuration, Palette Definitions, and Helpers for Elvira's Visual System
"""

import shutil
import re
from typing import Dict
from manim import MathTex, Text

# Klimt Palette Colors extracted from "The Kiss"
KLIMT_PALETTE: Dict[str, str] = {
    "Gold": "#D4AF37",
    "GoldLight": "#F5E6BE",
    "Ochre": "#B58E43",
    "Lapis": "#2B5A75",
    "Crimson": "#C02B37",
    "Emerald": "#2E6B56",
    "Obsidian": "#1A1815",
    "Alabaster": "#F5F0E6",
}

KLIMT_GOLD = KLIMT_PALETTE["Gold"]
KLIMT_GOLD_LIGHT = KLIMT_PALETTE["GoldLight"]
KLIMT_OCHRE = KLIMT_PALETTE["Ochre"]
KLIMT_LAPIS = KLIMT_PALETTE["Lapis"]
KLIMT_CRIMSON = KLIMT_PALETTE["Crimson"]
KLIMT_EMERALD = KLIMT_PALETTE["Emerald"]
KLIMT_OBSIDIAN = KLIMT_PALETTE["Obsidian"]
KLIMT_ALABASTER = KLIMT_PALETTE["Alabaster"]

# Typography Defaults (Strictly Upright Roman Styles)
FONT_SERIF = "Cormorant Garamond"
FONT_SANS = "Plus Jakarta Sans"
FONT_MONO = "Fira Code"

# Aspect Ratio Frame Specs
ASPECT_RATIOS: Dict[str, Dict[str, float]] = {
    "9:16": {
        "pixel_width": 1080,
        "pixel_height": 1920,
        "frame_width": 9.0,
        "frame_height": 16.0,
        "card_scale": 0.85,
        "font_scale": 0.85,
    },
    "16:9": {
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_width": 16.0,
        "frame_height": 9.0,
        "card_scale": 1.0,
        "font_scale": 1.0,
    },
}

def get_aspect_config(ratio_key: str = "9:16") -> Dict[str, float]:
    """Return aspect ratio configuration dictionary for Manim setup."""
    return ASPECT_RATIOS.get(ratio_key, ASPECT_RATIOS["9:16"])

def is_latex_available() -> bool:
    """Check if latex executable is installed on PATH."""
    return shutil.which("latex") is not None or shutil.which("xelatex") is not None

def format_latex_to_unicode(latex_str: str) -> str:
    """
    Convert raw LaTeX math strings into high-fidelity mathematical text
    with genuine Unicode mathematical operators and subscripts.
    """
    s = latex_str.strip()

    replacements = [
        (r'\\boldsymbol\{\\theta\}', 'θ'),
        (r'\\nabla_{\\boldsymbol\{\\theta\}}', '∇_θ'),
        (r'\\nabla_{\\theta}', '∇_θ'),
        (r'\\mathcal\{L\}', 'ℒ'),
        (r'\\mathbf\{([A-Za-z])\}', r'\1'),
        (r'\\mathbf\{([A-Za-z]+)\}', r'\1'),
        (r'\\mathrm\{([A-Za-z]+)\}', r'\1'),
        (r'\\text\{([A-Za-z]+)\}', r'\1'),
        (r'\\left', ''),
        (r'\\right', ''),
        (r'\\,', ' '),
        (r'\\bigcup_\{i=1\}\^\{?\\infty\}?', '⋃ᵢ₌₁^∞'),
        (r'\\sum_\{i=1\}\^\{?\\infty\}?', '∑ᵢ₌₁^∞'),
        (r'\\sum_\{i=1\}\^\{?n\}?', '∑ᵢ₌₁ⁿ'),
        (r'\\sum_\{k=1\}\^\{?n\}?', '∑ₖ₌₁ⁿ'),
        (r'\\bigcup_\{i=1\}', '⋃ᵢ₌₁'),
        (r'\\sum_\{i=1\}', '∑ᵢ₌₁'),
        (r'\\bigcup', '⋃'),
        (r'\\bigcap', '⋂'),
        (r'\\sum', '∑'),
        (r'\\int', '∫'),
        (r'\\mu', 'μ'),
        (r'\\nu', 'ν'),
        (r'\\theta', 'θ'),
        (r'\\eta', 'η'),
        (r'\\nabla', '∇'),
        (r'\\Sigma', 'Σ'),
        (r'\\sigma', 'σ'),
        (r'\\lambda', 'λ'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\epsilon', 'ε'),
        (r'\\delta', 'δ'),
        (r'\\pi', 'π'),
        (r'\\infty', '∞'),
        (r'\\mathbb\{R\}', 'ℝ'),
        (r'\\in', '∈'),
        (r'\\notin', '∉'),
        (r'\\subset', '⊂'),
        (r'\\subseteq', '⊆'),
        (r'\\approx', '≈'),
        (r'\\neq', '≠'),
        (r'\\le', '≤'),
        (r'\\ge', '≥'),
        (r'\\times', '×'),
        (r'\\cdot', '·'),
        (r'\\pm', '±'),
        (r'\\sqrt', '√'),
        (r'\\sim', '∼'),
        (r'\\to', '→'),
        (r'\\mid', '∣'),
        (r'\\top', 'ᵀ'),
        (r'_\{t\+1\}', 'ₜ₊₁'),
        (r'_\{i\}', 'ᵢ'),
        (r'_\{j\}', 'ⱼ'),
        (r'_\{k\}', 'ₖ'),
        (r'_\{n\}', 'ₙ'),
        (r'_\{t\}', 'ₜ'),
        (r'_\{0\}', '₀'),
        (r'_\{1\}', '₁'),
        (r'_\{2\}', '₂'),
        (r'_\{3\}', '₃'),
        (r'_\{4\}', '₄'),
        (r'_\{5\}', '₅'),
        (r'_i\b', 'ᵢ'),
        (r'_j\b', 'ⱼ'),
        (r'_k\b', 'ₖ'),
        (r'_n\b', 'ₙ'),
        (r'_0\b', '₀'),
        (r'_1\b', '₁'),
        (r'_2\b', '₂'),
        (r'_3\b', '₃'),
        (r'_4\b', '₄'),
        (r'_5\b', '₅'),
        (r'_t\b', 'ₜ'),
    ]
    for pattern, rep in replacements:
        s = re.sub(pattern, rep, s)

    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1 / \2)', s)
    s = re.sub(r'[\{\}\\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def create_math_mobject(formula_str: str, font_size: int = 52, color: str = KLIMT_GOLD_LIGHT, max_width: float = 12.0, **kwargs):
    """
    Create MathTex Mobject if LaTeX is installed, otherwise fallback to beautifully
    typeset mathematical Text using Windows Cambria Math / Segoe UI Symbol.
    """
    if is_latex_available():
        try:
            mob = MathTex(formula_str, color=color, font_size=font_size, **kwargs)
            if max_width and mob.width > max_width:
                mob.scale_to_fit_width(max_width)
            return mob
        except Exception:
            pass

    readable_text = format_latex_to_unicode(formula_str)
    font_stack = ["Cambria Math", "Segoe UI Symbol", "Georgia", "Times New Roman", FONT_SERIF]
    mob = None
    for f in font_stack:
        try:
            mob = Text(readable_text, color=color, font_size=font_size, font=f, **kwargs)
            break
        except Exception:
            pass
    if mob is None:
        mob = Text(readable_text, color=color, font_size=font_size, **kwargs)

    if max_width and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob
