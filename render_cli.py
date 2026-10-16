"""
CLI Rendering Utility for Elvira's Brand System Scenes
"""

import argparse
import sys
import os
import subprocess
from typing import List

SCENE_MAP = [
    "MeasureTheoryOverlayScene",
    "MatrixTransformerScene",
    "GradientDescentLandscapeScene",
]

def build_manim_cmd(
    scene_name: str = "MeasureTheoryOverlayScene",
    aspect_ratio: str = "9:16",
    quality: str = "low",
    transparent: bool = False,
    bg: str = "dark",
) -> List[str]:
    """Helper to construct Manim CLI command list for rendering."""
    q_flag = {
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh",
        "fourk": "-qk",
    }.get(quality, "-ql")

    w, h = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
    bg_mode = "transparent" if transparent else bg

    cmd = [
        sys.executable,
        "-m",
        "manim",
        "elvira_manim/scenes/demo_scenes.py",
        scene_name,
        q_flag,
        "-r",
        f"{w},{h}",
        "--disable_caching",
    ]
    if bg_mode == "transparent":
        cmd.extend(["-t", "--format", "webm"])

    return cmd

def main():
    parser = argparse.ArgumentParser(
        description="Render Elvira Brand System Manim animations with Klimt styling."
    )
    parser.add_argument(
        "--scene",
        choices=SCENE_MAP,
        default="MeasureTheoryOverlayScene",
        help="Name of the scene to render.",
    )
    parser.add_argument(
        "--aspect",
        choices=["9:16", "16:9"],
        default="9:16",
        help="Aspect ratio: 9:16 (vertical Reels/TikTok) or 16:9 (horizontal YouTube).",
    )
    parser.add_argument(
        "--bg",
        choices=["dark", "light", "transparent"],
        default="dark",
        help="Background mode: dark (Obsidian #1A1815), light (Alabaster #F5F0E6), or transparent (Alpha for video overlays).",
    )
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high", "fourk"],
        default="low",
        help="Render quality (low=480p/15fps, medium=720p/30fps, high=1080p/60fps).",
    )
    parser.add_argument(
        "--transparent",
        "-t",
        action="store_true",
        help="Shorthand flag to force transparent background mode.",
    )

    args = parser.parse_args()

    bg_mode = "transparent" if args.transparent else args.bg
    cmd = build_manim_cmd(
        scene_name=args.scene,
        aspect_ratio=args.aspect,
        quality=args.quality,
        transparent=args.transparent,
        bg=args.bg,
    )

    env = os.environ.copy()
    env["ELVIRA_ASPECT_RATIO"] = args.aspect
    env["ELVIRA_BG_MODE"] = bg_mode

    print(f"[ELVIRA MANIM RENDERER] Executing command: {' '.join(cmd)}")
    print(f"[ELVIRA MANIM RENDERER] Environment: ASPECT={args.aspect}, BG={bg_mode}")
    subprocess.run(cmd, env=env, check=True)

if __name__ == "__main__":
    main()
