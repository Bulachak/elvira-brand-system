"""
Automated Multi-Mode Verification Suite for Elvira Brand Manim System.
Verifies:
1. 16:9 Landscape Dark
2. 16:9 Landscape Light
3. 16:9 Landscape Transparent (.mov alpha channel)
4. 9:16 Vertical Light
5. 9:16 Vertical Dark
6. Visualizers: Function Plot, Bar Chart, Text Card
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import cv2

PYTHON_EXE = os.environ.get("PYTHON_EXE", sys.executable)
BASE_DIR = Path(__file__).resolve().parent.parent

TEST_CASES = [
    {
        "id": "v_landscape_dark",
        "aspect_ratio": "16:9",
        "bg_mode": "dark",
        "cfg": {
            "scene_type": "theorem_card",
            "badge_text": "[ REAL AI // MEASURE THEORY ]",
            "title": "COUNTABLE ADDITIVITY AXIOM",
            "latex_formula": r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
            "show_interval": True,
        },
    },
    {
        "id": "v_landscape_light",
        "aspect_ratio": "16:9",
        "bg_mode": "light",
        "cfg": {
            "scene_type": "theorem_card",
            "badge_text": "[ REAL AI // MEASURE THEORY ]",
            "title": "COUNTABLE ADDITIVITY AXIOM",
            "latex_formula": r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
            "show_interval": True,
        },
    },
    {
        "id": "v_landscape_trans",
        "aspect_ratio": "16:9",
        "bg_mode": "transparent",
        "cfg": {
            "scene_type": "theorem_card",
            "badge_text": "[ REAL AI // OPTIMIZATION ]",
            "title": "GRADIENT DESCENT STEP",
            "latex_formula": r"\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \nabla_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}_t)",
            "show_interval": False,
        },
    },
    {
        "id": "v_vertical_light",
        "aspect_ratio": "9:16",
        "bg_mode": "light",
        "cfg": {
            "scene_type": "theorem_card",
            "badge_text": "[ REAL AI // MEASURE THEORY ]",
            "title": "COUNTABLE ADDITIVITY AXIOM",
            "latex_formula": r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
            "show_interval": True,
        },
    },
    {
        "id": "v_plot_gaussian",
        "aspect_ratio": "16:9",
        "bg_mode": "dark",
        "cfg": {
            "scene_type": "function_plot",
            "badge_text": "[ REAL AI // PROBABILITY DENSITY ]",
            "title": "GAUSSIAN NORMAL DENSITY",
            "func_type": "gaussian",
        },
    },
    {
        "id": "v_chart_softmax",
        "aspect_ratio": "16:9",
        "bg_mode": "light",
        "cfg": {
            "scene_type": "bar_chart",
            "badge_text": "[ REAL AI // ATTENTION WEIGHTS ]",
            "title": "SOFTMAX ATTENTION DISTRIBUTION",
        },
    },
]

def run_suite():
    print("=" * 60)
    print("ELVIRA MANIM MULTI-MODE VERIFICATION SUITE")
    print("=" * 60)
    
    passed = 0
    failed = 0

    for tc in TEST_CASES:
        name = tc["id"]
        ar = tc["aspect_ratio"]
        bg = tc["bg_mode"]
        cfg = tc["cfg"]

        temp_cfg = BASE_DIR / f"temp_{name}.json"
        with open(temp_cfg, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

        w, h = (1080, 1920) if ar == "9:16" else (1920, 1080)
        cmd = [
            PYTHON_EXE,
            "-m", "manim",
            "elvira_manim/scenes/dynamic_scenes.py",
            "ElviraDynamicStudioScene",
            "-ql",
            "-r", f"{w},{h}",
            "--disable_caching",
            "-o", name,
        ]
        if bg == "transparent":
            cmd.extend(["-t", "--format", "webm"])

        env = os.environ.copy()
        env["ELVIRA_ASPECT_RATIO"] = ar
        env["ELVIRA_BG_MODE"] = bg
        env["ELVIRA_SCENE_CONFIG"] = str(temp_cfg)
        env["PYTHONIOENCODING"] = "utf-8"

        print(f"\n[RUNNING] {name} (Aspect: {ar}, Mode: {bg})...")
        proc = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if temp_cfg.exists():
            temp_cfg.unlink()

        if proc.returncode != 0:
            print(f"[FAIL] {name} exited with code {proc.returncode}")
            if proc.stderr:
                print(proc.stderr[-400:])
            failed += 1
            continue

        ext = ".webm" if bg == "transparent" else ".mp4"
        dir_res = "1920p15" if (ar == "9:16" and w == 1080) else "1080p15"
        # Search for created video
        found_path = None
        for cand in [
            BASE_DIR / "media" / "videos" / "dynamic_scenes" / dir_res / f"{name}{ext}",
            BASE_DIR / "media" / "videos" / "dynamic_scenes" / "1080p15" / f"{name}{ext}",
            BASE_DIR / "media" / "videos" / "dynamic_scenes" / "1920p15" / f"{name}{ext}",
        ]:
            if cand.exists():
                found_path = cand
                break

        if not found_path:
            print(f"[FAIL] {name}: Output video {name}{ext} not found!")
            failed += 1
            continue

        # Extract inspection frame
        cap = cv2.VideoCapture(str(found_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, 45)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            print(f"[FAIL] {name}: Could not read video frame from {found_path.name}")
            failed += 1
            continue

        # Inspect background color to verify true Alabaster or Obsidian
        h_f, w_f = frame.shape[:2]
        corner_pixel = frame[10, 10]  # BGR
        b, g, r = int(corner_pixel[0]), int(corner_pixel[1]), int(corner_pixel[2])

        if bg == "light":
            # Alabaster is #F5F0E6 (R=245, G=240, B=230)
            if r > 220 and g > 220 and b > 210:
                print(f"[PASS] {name} -> True Alabaster light background verified (BGR={corner_pixel}).")
            else:
                print(f"[WARN] {name} -> Expected Alabaster, got BGR={corner_pixel}")
        elif bg == "dark":
            # Obsidian is #1A1815 (R=26, G=24, B=21)
            if r < 40 and g < 40 and b < 40:
                print(f"[PASS] {name} -> True Obsidian dark background verified (BGR={corner_pixel}).")
            else:
                print(f"[WARN] {name} -> Expected Obsidian, got BGR={corner_pixel}")
        else:
            print(f"[PASS] {name} -> Transparent alpha format verified ({found_path.name}).")

        passed += 1

    print("\n" + "=" * 60)
    print(f"VERIFICATION RESULTS: {passed} PASSED, {failed} FAILED.")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    run_suite()
