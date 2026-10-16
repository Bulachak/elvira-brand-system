"""
Elvira Brand System - Interactive Mathematical Animation Studio
FastAPI backend and live web UI for rendering Klimt-styled mathematical
animations, formulas, graph charts, text nodes, and video overlays with Manim.
"""

import os
import sys
import json
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Project root directory
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
VIDEOS_DIR = MEDIA_DIR / "videos"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# Detect Python interpreter with Manim installed
def find_manim_python() -> str:
    env_python = os.environ.get("PYTHON_EXE", "").strip()
    if env_python and Path(env_python).exists():
        return env_python

    try:
        res = subprocess.run([sys.executable, "-c", "import manim; print('OK')"], capture_output=True, text=True, timeout=5)
        if "OK" in res.stdout:
            return sys.executable
    except Exception:
        pass

    return "python"

PYTHON_EXE = find_manim_python()
print(f"[ELVIRA STUDIO] Using Python interpreter: {PYTHON_EXE}")

app = FastAPI(title="Elvira Brand System - Math & Infographic Studio", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media directory to serve videos directly
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Mount deliverables package directory if present
DELIVERABLES_DIR = BASE_DIR / "deliverables"
if DELIVERABLES_DIR.exists():
    app.mount("/deliverables", StaticFiles(directory=str(DELIVERABLES_DIR), html=True), name="deliverables")

@app.get("/brand", response_class=HTMLResponse)
@app.get("/aesthetic_canvas_klimt_ml_brand_system.html", response_class=HTMLResponse)
async def serve_brand_canvas():
    brand_file = BASE_DIR / "aesthetic_canvas_klimt_ml_brand_system.html"
    if brand_file.exists():
        return HTMLResponse(content=brand_file.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Brand guidelines HTML not found.")

@app.get("/carousel", response_class=HTMLResponse)
@app.get("/instagram_carousel_generator.html", response_class=HTMLResponse)
async def serve_carousel_generator():
    carousel_file = BASE_DIR / "instagram_carousel_generator.html"
    if carousel_file.exists():
        return HTMLResponse(content=carousel_file.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Instagram Carousel Generator HTML not found.")

import urllib.request
import urllib.error

@app.get("/favicon.svg")
@app.get("/favicon.ico")
async def serve_favicon():
    fav_file = BASE_DIR / "favicon.svg"
    if fav_file.exists():
        return FileResponse(str(fav_file), media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon not found.")

CUSTOM_DECK_FILE = BASE_DIR / "custom_carousel.json"

@app.get("/api/carousel-deck")
async def get_custom_carousel_deck():
    if CUSTOM_DECK_FILE.exists():
        try:
            data = json.loads(CUSTOM_DECK_FILE.read_text(encoding="utf-8"))
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid custom_carousel.json: {e}")
    raise HTTPException(status_code=404, detail="No custom_carousel.json pushed yet. Have your local AI agent POST to /api/carousel-deck or write custom_carousel.json.")

@app.post("/api/carousel-deck")
async def save_custom_carousel_deck(request: Request):
    try:
        payload = await request.json()
        CUSTOM_DECK_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return JSONResponse(content={"status": "ok", "saved_to": str(CUSTOM_DECK_FILE)})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ai-generate")
async def proxy_ai_generate(request: Request):
    """
    Optional local server AI bridge: uses either user-provided api_key in payload
    or local environment variable (GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY).
    Zero hardcoded credentials.
    """
    body = await request.json()
    provider = (body.get("provider") or "gemini").lower()
    model = body.get("model") or "gemini-2.5-flash"
    prompt = body.get("prompt") or ""
    api_key = (body.get("api_key") or "").strip()

    env_map = {
        "gemini": "GEMINI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    if not api_key and provider in env_map:
        api_key = os.environ.get(env_map[provider], "").strip()

    if not api_key and provider != "ollama":
        raise HTTPException(
            status_code=400,
            detail=f"No API key entered in browser and {env_map.get(provider, 'API_KEY')} is not set in local environment. Paste your key in the studio or use the External AI Agent tab."
        )

    try:
        if provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "responseMimeType": "application/json"}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                return JSONResponse(content={"text": text})

        elif provider == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            req_data = json.dumps({
                "model": model,
                "max_tokens": 4096,
                "temperature": 0.4,
                "messages": [{"role": "user", "content": prompt}]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                text = resp_json["content"][0]["text"]
                return JSONResponse(content={"text": text})

        else:
            url = "https://api.openai.com/v1/chat/completions" if provider == "openai" else (
                "https://openrouter.ai/api/v1/chat/completions" if provider == "openrouter" else "http://localhost:11434/v1/chat/completions"
            )
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            req_data = json.dumps({
                "model": model,
                "temperature": 0.4,
                "messages": [{"role": "user", "content": prompt}]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                text = resp_json["choices"][0]["message"]["content"]
                return JSONResponse(content={"text": text})
    except urllib.error.HTTPError as he:
        err_body = he.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=he.code, detail=f"Provider HTTP {he.code}: {err_body}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/klimt-assets/{filename}")
async def serve_klimt_asset(filename: str):
    safe_name = Path(filename).name
    target = BASE_DIR / safe_name
    if target.exists() and target.suffix.lower() in {".png", ".svg", ".jpg", ".jpeg", ".webp"}:
        return FileResponse(str(target))
    raise HTTPException(status_code=404, detail="Asset not found.")

@app.get("/files", response_class=HTMLResponse)
async def serve_video_gallery():
    videos = sorted(
        list(VIDEOS_DIR.glob("**/*.mp4")) + list(VIDEOS_DIR.glob("**/*.webm")),
        key=os.path.getmtime,
        reverse=True,
    )
    items_html = ""
    for v in videos:
        if "partial_movie_files" in v.parts:
            continue
        rel = v.relative_to(MEDIA_DIR).as_posix()
        url = f"/media/{rel}"
        size_kb = v.stat().st_size / 1024
        ext = v.suffix.upper().lstrip(".")
        badge_col = "#2E6B56" if ext == "WEBM" else "#2B5A75"
        badge_label = "WEBM · ALPHA" if ext == "WEBM" else "MP4 · SOLID"
        items_html += f"""
        <div class="bg-white border border-[#DED6C5] rounded-xl p-5 flex flex-col justify-between gap-3 shadow-sm hover:border-[#1A1815] transition">
          <div>
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="px-2.5 py-0.5 rounded-md text-[10px] font-mono font-bold text-white" style="background:{badge_col}">{badge_label}</span>
              <span class="text-[11px] font-mono text-[#4A4842] font-semibold">{size_kb:.1f} KB</span>
            </div>
            <div class="font-mono text-xs text-[#1A1815] font-bold break-all">{v.name}</div>
            <div class="font-mono text-[10px] text-[#4A4842] mt-1">{rel}</div>
          </div>
          <div class="flex gap-2 mt-2">
            <a href="{url}" target="_blank" class="flex-1 text-center px-3 py-2 rounded-lg border border-[#DED6C5] bg-[#F5F0E6] text-xs font-mono font-bold text-[#1A1815] hover:border-[#1A1815]">Open</a>
            <a href="{url}" download="{v.name}" class="flex-1 text-center px-3 py-2 rounded-lg bg-[#1A1815] text-[#F5F0E6] border border-[#D4AF37] text-xs font-mono font-bold hover:bg-[#2B5A75]">Download</a>
          </div>
        </div>
        """
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Elvira Astashkina — Rendered Video Archive</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #F5F0E6;
      background-image:
        radial-gradient(rgba(212, 175, 55, 0.14) 1px, transparent 0),
        radial-gradient(rgba(43, 90, 117, 0.07) 1px, transparent 0);
      background-size: 28px 28px;
      background-position: 0 0, 14px 14px;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
  </style>
</head>
<body class="text-[#1A1815] min-h-screen">
  <header class="border-b border-[#DED6C5] px-6 py-4 bg-white/95 backdrop-blur-md sticky top-0 z-40 shadow-sm">
    <div class="max-w-7xl mx-auto flex justify-between items-center gap-4">
      <a href="/" class="flex items-center gap-3">
        <img src="/deliverables/assets/logo-horizontal-light.svg" alt="Elvira Astashkina" class="h-10 w-auto">
      </a>
      <div class="flex gap-2">
        <a href="/" class="px-3.5 py-2 rounded-lg border border-[#DED6C5] bg-[#F5F0E6] text-[#1A1815] text-xs font-bold uppercase tracking-wider">← Brand Hub</a>
        <a href="/video" class="px-3.5 py-2 rounded-lg bg-[#1A1815] text-[#F5F0E6] border border-[#D4AF37] text-xs font-bold uppercase tracking-wider">← Back to Video Studio</a>
      </div>
    </div>
  </header>
  <div class="max-w-7xl mx-auto p-8">
    <div class="mb-6 border-b border-[#DED6C5] pb-4">
      <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-[#2B5A75] font-bold">Motion Archive · media/videos/</span>
      <h1 class="text-3xl font-bold text-[#1A1815]" style="font-family:'Cormorant Garamond',serif;">Rendered Mathematical Animations</h1>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {items_html}
    </div>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)

PRESETS = [
    {
        "id": "gaussian_plot_dark",
        "name": "Gaussian Curve & Shaded Integral",
        "scene_type": "function_plot",
        "badge_text": "[ REAL AI // PROBABILITY DENSITY ]",
        "title": "NORMAL DENSITY FUNCTION",
        "subtitle": "CONTINUOUS GAUSSIAN MEASURE AREA",
        "latex_formula": r"f(x) = \frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}x^2}",
        "func_type": "gaussian",
        "aspect_ratio": "9:16",
        "bg_mode": "dark",
        "description": "Coordinate axes with golden Gaussian bell curve and Lapis teal shaded integral area.",
    },
    {
        "id": "sigmoid_landscape_light",
        "name": "Sigmoid Activation Curve",
        "scene_type": "function_plot",
        "badge_text": "[ REAL AI // NEURAL ACTIVATION ]",
        "title": "SIGMOID ACTIVATION FUNCTION",
        "subtitle": "NON-LINEAR PROJECTION TO PROBABILITY SPACE",
        "latex_formula": r"\sigma(x) = \frac{1}{1 + e^{-x}} \in (0, 1)",
        "func_type": "sigmoid",
        "aspect_ratio": "16:9",
        "bg_mode": "light",
        "description": "Landscape 16:9 YouTube format on Alabaster Light background with Ochre coordinates.",
    },
    {
        "id": "discrete_bar_chart",
        "name": "Discrete Softmax Bar Chart",
        "scene_type": "bar_chart",
        "badge_text": "[ REAL AI // ATTENTION PROBABILITY ]",
        "title": "SOFTMAX ATTENTION PROBABILITIES",
        "subtitle": "DISCRETE CATEGORICAL DISTRIBUTION P(Z = z_i)",
        "latex_formula": r"P(Z = z_i) = \frac{e^{w_i^\top x}}{\sum_j e^{w_j^\top x}}",
        "aspect_ratio": "9:16",
        "bg_mode": "transparent",
        "description": "Probability distribution bar chart in Klimt mosaic colors (Lapis, Gold, Crimson, Emerald).",
    },
    {
        "id": "text_concept_card",
        "name": "Conceptual Definition Card",
        "scene_type": "text_card",
        "badge_text": "[ REAL AI // MEASURE THEORY DEFINITION ]",
        "title": "MEASURABLE SPACE DEFINITION",
        "subtitle": "AXIOMATIC FOUNDATION",
        "latex_formula": "",
        "body_text": "A pair (X, Σ) where X is a non-empty set and Σ is a σ-algebra on X. Every element of Σ is a measurable set upon which probability can be formally integrated.",
        "aspect_ratio": "9:16",
        "bg_mode": "dark",
        "description": "High-contrast editorial card for conceptual explanations and text definitions.",
    },
    {
        "id": "countable_additivity",
        "name": "Countable Additivity Axiom",
        "scene_type": "theorem_card",
        "badge_text": "[ REAL AI // MEASURE THEORY ]",
        "title": "COUNTABLE ADDITIVITY AXIOM",
        "subtitle": "LEBESGUE MEASURE SPACE (X, Σ, μ)",
        "latex_formula": r"\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)",
        "aspect_ratio": "9:16",
        "bg_mode": "transparent",
        "show_interval": True,
        "description": "Klimt gold theorem card with countable additivity axiom and partitioned Lebesgue interval line.",
    },
    {
        "id": "vit_matrix_grid",
        "name": "Vision Transformer & Matrix Tiles",
        "scene_type": "matrix_grid",
        "badge_text": "[ REAL AI // TENSOR ARCHITECTURE ]",
        "title": "DISCRETE MATRIX TILES",
        "subtitle": "WEIGHT TENSORS W ∈ ℝ^(m × n) AND PATCH EMBEDDINGS",
        "latex_formula": r"\mathbf{z}_0 = [\mathbf{x}_{\text{class}}; \mathbf{x}_p^1 \mathbf{E}; \dots; \mathbf{x}_p^N \mathbf{E}] + \mathbf{E}_{\text{pos}}",
        "aspect_ratio": "16:9",
        "bg_mode": "dark",
        "matrix_rows": 4,
        "matrix_cols": 4,
        "description": "Rectilinear mosaic tile matrix illustrating discrete tokenization, weights, and patch blocks.",
    },
    {
        "id": "gradient_descent",
        "name": "Gradient Descent Loss Trajectory",
        "scene_type": "gradient_descent",
        "badge_text": "[ REAL AI // OPTIMIZATION LANDSCAPE ]",
        "title": "GRADIENT DESCENT LOSS TRAJECTORY",
        "subtitle": "FLOWING THROUGH MULTIDIMENSIONAL VALLEYS",
        "latex_formula": r"\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \nabla_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta})",
        "aspect_ratio": "9:16",
        "bg_mode": "transparent",
        "description": "Golden spiral loss landscape streamlines with directional descent vector arrows.",
    },
    {
        "id": "gaussian_density",
        "name": "Continuous Iso-Density Contours",
        "scene_type": "iso_density",
        "badge_text": "[ REAL AI // PROBABILITY SPACES ]",
        "title": "CONTINUOUS PROBABILITY FIELDS",
        "subtitle": "LATENT GAUSSIAN DENSITY p(x) & ISO-CONTOURS",
        "latex_formula": r"p(\mathbf{x}) = \frac{1}{(2\pi)^{d/2}|\mathbf{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^\top \mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right)",
        "aspect_ratio": "9:16",
        "bg_mode": "light",
        "num_contours": 4,
        "description": "Continuous concentric rings on Alabaster Light ground with Ochre and Lapis lines.",
    },
]

@app.get("/api/presets")
async def get_presets():
    return JSONResponse(PRESETS)

@app.post("/api/render")
async def render_scene(payload: Dict[str, Any]):
    """
    Renders a dynamic Manim scene based on the received JSON configuration.
    Supports dark, light, and transparent background modes in 9:16 and 16:9.
    """
    scene_type = payload.get("scene_type", "theorem_card")
    badge_text = payload.get("badge_text", "[ REAL AI // MATHEMATICS ]")
    title = payload.get("title", "COUNTABLE ADDITIVITY AXIOM")
    subtitle = payload.get("subtitle", "LEBESGUE MEASURE SPACE")
    latex_formula = payload.get("latex_formula", r"\mu(A \cup B) = \mu(A) + \mu(B)")
    body_text = payload.get("body_text", "")
    func_type = payload.get("func_type", "gaussian")
    custom_code = payload.get("custom_code", "")
    aspect_ratio = payload.get("aspect_ratio", "9:16")
    bg_mode = payload.get("bg_mode", "transparent")  # "dark", "light", "transparent"
    quality = payload.get("quality", "low")  # "low", "medium", "high"
    show_interval = bool(payload.get("show_interval", True))
    matrix_rows = int(payload.get("matrix_rows", 4))
    matrix_cols = int(payload.get("matrix_cols", 4))
    num_contours = int(payload.get("num_contours", 4))

    run_id = uuid.uuid4().hex[:8]
    config_file = BASE_DIR / f"temp_render_cfg_{run_id}.json"

    cfg_data = {
        "scene_type": scene_type,
        "badge_text": badge_text,
        "title": title,
        "subtitle": subtitle,
        "latex_formula": latex_formula,
        "body_text": body_text,
        "func_type": func_type,
        "custom_code": custom_code,
        "aspect_ratio": aspect_ratio,
        "bg_mode": bg_mode,
        "show_interval": show_interval,
        "matrix_rows": matrix_rows,
        "matrix_cols": matrix_cols,
        "num_contours": num_contours,
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg_data, f, indent=2)

    # Resolution & Quality flags
    q_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-ql")
    w, h = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
    
    cmd = [
        PYTHON_EXE,
        "-m",
        "manim",
        "elvira_manim/scenes/dynamic_scenes.py",
        "ElviraDynamicStudioScene",
        q_flag,
        "-r",
        f"{w},{h}",
        "--disable_caching",
    ]

    # Add transparency flag with VP9 WebM alpha if requested
    if bg_mode == "transparent":
        cmd.extend(["-t", "--format", "webm"])

    env = os.environ.copy()
    env["ELVIRA_ASPECT_RATIO"] = aspect_ratio
    env["ELVIRA_BG_MODE"] = bg_mode
    env["ELVIRA_SCENE_CONFIG"] = str(config_file)
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        print(f"[ELVIRA STUDIO] Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )

        # Cleanup temp config file
        if config_file.exists():
            config_file.unlink()

        if result.returncode != 0:
            print(f"[ELVIRA STUDIO] Error stderr:\n{result.stderr}")
            print(f"[ELVIRA STUDIO] Error stdout:\n{result.stdout}")
            raise HTTPException(status_code=500, detail=f"Manim rendering failed: {result.stderr or result.stdout}")

        # Search for generated movie file
        ext = "webm" if bg_mode == "transparent" else "mp4"
        expected_candidates = list(VIDEOS_DIR.glob(f"**/*ElviraDynamicStudioScene*.{ext}"))
        if not expected_candidates:
            expected_candidates = list(VIDEOS_DIR.glob(f"**/*.{ext}"))
        
        if not expected_candidates:
            raise HTTPException(status_code=500, detail="Animation rendered but output video file was not found on disk.")

        # Sort by modification time to get the newest file
        newest_video = max(expected_candidates, key=os.path.getmtime)
        rel_path = newest_video.relative_to(MEDIA_DIR).as_posix()
        web_url = f"/media/{rel_path}"

        return JSONResponse({
            "status": "success",
            "video_url": web_url,
            "filename": newest_video.name,
            "format": ext,
            "aspect_ratio": aspect_ratio,
            "bg_mode": bg_mode,
            "message": f"Successfully rendered {scene_type} animation ({aspect_ratio}, {bg_mode})."
        })

    except subprocess.TimeoutExpired:
        if config_file.exists():
            config_file.unlink()
        raise HTTPException(status_code=504, detail="Rendering timed out after 120 seconds.")
    except Exception as e:
        if config_file.exists():
            config_file.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def serve_main_deliverables_hub():
    """
    Serves the Brand Package Deliverables Hub ('Everything You Need — The Klimt × ML Archive')
    as the canonical Main Page (/).
    """
    hub_file = DELIVERABLES_DIR / "index.html"
    if hub_file.exists():
        return HTMLResponse(content=hub_file.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Deliverables hub index.html not found.")


@app.get("/bio", response_class=HTMLResponse)
@app.get("/link-in-bio", response_class=HTMLResponse)
async def serve_link_in_bio():
    bio_file = DELIVERABLES_DIR / "content-templates" / "link-in-bio.html"
    if bio_file.exists():
        return HTMLResponse(content=bio_file.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Link-in-bio template not found.")


@app.get("/newsletter", response_class=HTMLResponse)
async def serve_newsletter():
    nl_file = DELIVERABLES_DIR / "content-templates" / "email-newsletter-template.html"
    if nl_file.exists():
        return HTMLResponse(content=nl_file.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Email newsletter template not found.")


@app.get("/video", response_class=HTMLResponse)
@app.get("/studio", response_class=HTMLResponse)
async def serve_studio_ui():
    """
    Manim Mathematical Animation & Overlay Studio UI:
    Unified with the Warm Alabaster Parchment (#F5F0E6) gallery aesthetic,
    Horizontal Lockup header (Logo + Elvira Astashkina), Cormorant Garamond headings,
    and 100% WCAG AA/AAA contrast.
    """
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Elvira Astashkina — Manim Video &amp; Overlay Studio</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Elvira Astashkina (@elvrast)">
  <meta property="og:title" content="Elvira Astashkina — Manim Video &amp; Overlay Studio">
  <meta property="og:description" content="Elvira Astashkina (@elvrast) — Applied Machine Learning Engineer &amp; AI Educator in the San Francisco Bay Area. Where Mathematical Rigor Meets Editorial Clarity.">
  <meta property="og:image" content="https://elvira-brand-system.vercel.app/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Elvira Astashkina — Manim Video &amp; Overlay Studio">
  <meta name="twitter:description" content="Elvira Astashkina (@elvrast) — Applied Machine Learning Engineer &amp; AI Educator in the San Francisco Bay Area. Where Mathematical Rigor Meets Editorial Clarity.">
  <meta name="twitter:image" content="https://elvira-brand-system.vercel.app/og-image.png">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- KaTeX for live mathematical formula preview -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>

  <!-- Google Fonts: Cormorant Garamond, Plus Jakarta Sans, Cinzel, JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Cinzel:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
            cinzel: ['"Cinzel"', 'serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            klimt: {
              gold: '#D4AF37',
              goldLight: '#F5E6BE',
              ochre: '#7A5B14',
              lapis: '#2B5A75',
              crimson: '#C02B37',
              emerald: '#2E6B56',
              obsidian: '#1A1815',
              alabaster: '#F5F0E6',
              clay: '#DED6C5',
              charcoal: '#22201D',
              slate: '#4A4842',
            }
          }
        }
      }
    }
  </script>

  <style>
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #F5F0E6; }
    ::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 3px; }

    /* Unified Warm Alabaster Parchment Gallery Canvas (matches Main Page & Brand System) */
    .klimt-texture {
      background-color: #F5F0E6;
      background-image:
        radial-gradient(rgba(212, 175, 55, 0.14) 1px, transparent 0),
        radial-gradient(rgba(43, 90, 117, 0.07) 1px, transparent 0);
      background-size: 28px 28px;
      background-position: 0 0, 14px 14px;
    }
    .checkboard-bg {
      background-color: #12100E;
      background-image: linear-gradient(45deg, #1c1915 25%, transparent 25%),
                        linear-gradient(-45deg, #1c1915 25%, transparent 25%),
                        linear-gradient(45deg, transparent 75%, #1c1915 75%),
                        linear-gradient(-45deg, transparent 75%, #1c1915 75%);
      background-size: 20px 20px;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
    }
    .light-preview-bg {
      background-color: #F5F0E6;
    }
    .dark-preview-bg {
      background-color: #1A1815;
    }
    h1, h2, h3, h4 { text-wrap: balance; }
    p { text-wrap: pretty; }
  </style>
</head>
<body class="klimt-texture text-klimt-obsidian min-h-screen font-sans selection:bg-klimt-gold selection:text-klimt-obsidian flex flex-col justify-between">

  <!-- Unified Editorial Header: Horizontal Lockup (Logo + First & Last Name Only) -->
  <header class="border-b border-klimt-clay px-5 py-3.5 md:px-12 bg-white/95 backdrop-blur-md sticky top-0 z-40 shadow-sm">
    <div class="max-w-[1560px] mx-auto flex flex-col lg:flex-row justify-between items-center gap-4">
      <a href="/" class="flex items-center gap-3.5 group shrink-0" aria-label="Elvira Astashkina">
        <svg class="w-10 h-10 rounded-lg shadow-sm border border-klimt-obsidian group-hover:scale-105 transition shrink-0" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="2" width="60" height="60" rx="10" fill="#F5F0E6" stroke="#1A1815" stroke-width="3.5"/>
          <rect x="8" y="8" width="20" height="26" rx="2" fill="#1A1815"/>
          <rect x="16" y="12" width="4" height="18" fill="#D4AF37"/>
          <rect x="8" y="38" width="20" height="10" rx="1.5" fill="#D4AF37" stroke="#1A1815" stroke-width="1"/>
          <rect x="8" y="50" width="20" height="6" rx="1.5" fill="#2B5A75"/>
          <line x1="32" y1="6" x2="32" y2="58" stroke="#1A1815" stroke-width="2"/>
          <circle cx="46" cy="24" r="11" fill="#C02B37" stroke="#1A1815" stroke-width="2"/>
          <circle cx="46" cy="24" r="5" fill="#F5F0E6"/>
          <circle cx="46" cy="47" r="8" fill="#2B5A75" stroke="#D4AF37" stroke-width="2"/>
          <circle cx="46" cy="47" r="3.2" fill="#2E6B56"/>
        </svg>
        <span class="text-2xl md:text-[26px] font-serif font-bold tracking-tight text-klimt-obsidian whitespace-nowrap">
          Elvira Astashkina
        </span>
      </a>

      <nav class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 w-full lg:w-auto justify-end text-xs font-bold uppercase tracking-wider">
        <a href="/" class="px-3.5 py-2 rounded-lg border border-klimt-clay bg-klimt-alabaster hover:border-klimt-obsidian text-klimt-obsidian text-center whitespace-nowrap transition">← Brand Hub</a>
        <a href="/brand" class="px-3.5 py-2 rounded-lg bg-white text-klimt-obsidian border border-klimt-clay hover:border-klimt-obsidian text-center whitespace-nowrap transition">Brand Canvas</a>
        <a href="/deliverables/brand-book/elvira-astashkina-2026-10-brand-book.html" class="px-3.5 py-2 rounded-lg bg-white text-klimt-obsidian border border-klimt-clay hover:border-klimt-obsidian text-center whitespace-nowrap transition">Brand Book</a>
        <a href="/carousel" class="px-3.5 py-2 rounded-lg bg-white text-klimt-obsidian border border-klimt-clay hover:border-klimt-obsidian text-center whitespace-nowrap transition">Carousel Studio</a>
        <a href="/files" class="px-3.5 py-2 rounded-lg bg-klimt-obsidian text-klimt-alabaster border border-klimt-gold hover:bg-klimt-lapis text-center whitespace-nowrap transition">Video Archive</a>
      </nav>
    </div>
  </header>

  <!-- Studio Title Banner -->
  <section class="max-w-[1560px] mx-auto w-full px-5 md:px-10 pt-8 pb-2">
    <div class="bg-white/95 rounded-2xl border border-klimt-clay p-6 md:p-8 shadow-sm flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
      <div class="space-y-2 max-w-3xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-md border border-klimt-clay bg-klimt-alabaster text-klimt-obsidian text-[10px] font-mono uppercase tracking-[0.2em] font-bold whitespace-nowrap">
          <span class="w-2 h-2 rounded-sm bg-klimt-lapis shrink-0"></span>
          <span>Manim Mathematical Motion Engine · 9:16 Reels &amp; 16:9 Lectures</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-serif font-normal text-klimt-obsidian leading-tight">
          Mathematical Video &amp; <span class="italic font-semibold text-klimt-lapis">Alpha Overlay</span> Studio.
        </h1>
        <p class="text-xs md:text-sm text-klimt-slate leading-relaxed">
          Compile publication-grade Manim animations, probability density curves, discrete matrix grids, and transparent VP9 alpha video overlays (<code class="font-mono text-klimt-obsidian bg-klimt-alabaster px-1.5 py-0.5 rounded">.webm</code> &amp; <code class="font-mono text-klimt-obsidian bg-klimt-alabaster px-1.5 py-0.5 rounded">.mp4</code>) styled in the 6-Tone Spectrum of Gustav Klimt’s <em>“The Kiss”</em>.
        </p>
      </div>
      <div class="flex flex-nowrap gap-2.5 shrink-0">
        <span class="px-3 py-1.5 rounded-lg bg-klimt-alabaster border border-klimt-clay font-mono text-[11px] font-bold text-klimt-obsidian whitespace-nowrap">VP9 Alpha .WEBM</span>
        <span class="px-3 py-1.5 rounded-lg bg-klimt-alabaster border border-klimt-clay font-mono text-[11px] font-bold text-klimt-obsidian whitespace-nowrap">Obsidian #1A1815</span>
        <span class="px-3 py-1.5 rounded-lg bg-klimt-alabaster border border-klimt-clay font-mono text-[11px] font-bold text-klimt-obsidian whitespace-nowrap">Alabaster #F5F0E6</span>
      </div>
    </div>
  </section>

  <!-- Main Studio Workspace (Balanced 6/6 Column Split for Generous Preview Stage) -->
  <main class="max-w-[1560px] mx-auto w-full px-5 md:px-10 py-6 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start">
    
    <!-- Left Column: Controls & Formula Editor (6 Cols) -->
    <div class="lg:col-span-6 space-y-6">

      <!-- 00. AI Model & Agent Scene Assistant -->
      <div class="bg-white border border-klimt-clay rounded-2xl p-6 shadow-md space-y-4">
        <div class="border-b border-klimt-clay pb-3 space-y-1.5">
          <div class="flex justify-between items-center gap-3">
            <span class="px-2.5 py-0.5 rounded-md bg-klimt-obsidian text-klimt-gold text-[10px] font-mono font-bold whitespace-nowrap shrink-0">BYOK + AGENT</span>
            <span class="text-[10px] font-mono text-klimt-ochre font-bold uppercase tracking-wider whitespace-nowrap shrink-0">Use Your Own AI Key or Agent</span>
          </div>
          <h2 class="text-xl font-serif font-bold text-klimt-obsidian whitespace-nowrap">
            00. AI Mathematical Scene Architect
          </h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          <select id="manim-ai-provider" onchange="onManimAiProviderChange()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs font-semibold rounded-lg px-3 py-2.5 font-mono focus:outline-none focus:border-klimt-obsidian">
            <option value="gemini">Google Gemini</option>
            <option value="anthropic">Anthropic Claude</option>
            <option value="openai">OpenAI (GPT / o-series)</option>
            <option value="openrouter">OpenRouter</option>
            <option value="ollama">Local Ollama (No Key)</option>
          </select>
          <input type="text" id="manim-ai-model" value="gemini-2.5-flash" placeholder="Model ID" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs font-semibold rounded-lg px-3 py-2.5 font-mono focus:outline-none focus:border-klimt-obsidian">
          <input type="password" id="manim-ai-key" oninput="saveManimAiPrefs()" placeholder="Your API Key (saved locally)" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs rounded-lg px-3 py-2.5 font-mono focus:outline-none focus:border-klimt-obsidian">
        </div>
        <div class="space-y-2 sm:space-y-0 sm:flex sm:gap-2.5">
          <input type="text" id="manim-ai-prompt" placeholder="Describe the math concept or formula (e.g., Bayes Theorem posterior update)..." class="w-full sm:flex-1 bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs rounded-lg px-3.5 py-2.5 font-sans focus:outline-none focus:border-klimt-obsidian">
          <div class="grid grid-cols-2 sm:flex gap-2">
            <button onclick="generateManimSceneWithAI()" id="btn-manim-ai" class="w-full sm:w-auto px-4 py-2.5 rounded-lg bg-klimt-obsidian hover:bg-klimt-lapis text-klimt-alabaster border border-klimt-gold text-xs font-mono font-bold uppercase tracking-wider transition whitespace-nowrap text-center">
              ✦ Draft with AI
            </button>
            <button onclick="copyManimAgentPrompt()" class="w-full sm:w-auto px-3.5 py-2.5 rounded-lg bg-klimt-alabaster hover:bg-white text-klimt-obsidian border border-klimt-clay hover:border-klimt-obsidian text-xs font-mono font-bold transition whitespace-nowrap text-center" title="Copy prompt for Claude Desktop, ChatGPT, Cursor, or Codex">
              Copy Agent Prompt
            </button>
          </div>
        </div>
        <div id="manim-ai-status" class="hidden text-[11px] font-mono text-klimt-obsidian bg-klimt-alabaster px-3.5 py-2 rounded-lg border border-klimt-clay font-semibold"></div>
      </div>
      
      <!-- 01. Preset Gallery Card -->
      <div class="bg-white border border-klimt-clay rounded-2xl p-6 shadow-md">
        <div class="border-b border-klimt-clay pb-3 mb-4 space-y-1">
          <div class="flex justify-between items-center gap-3">
            <span class="text-[10px] font-mono uppercase tracking-[0.2em] text-klimt-lapis font-bold whitespace-nowrap">Curated Scene Library</span>
            <span class="text-[11px] text-klimt-slate font-mono font-semibold whitespace-nowrap shrink-0">1-Click Load</span>
          </div>
          <h2 class="text-xl font-serif font-bold text-klimt-obsidian whitespace-nowrap">01. Mathematics, Graphs &amp; Concept Presets</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5" id="preset-container">
          <!-- Populated dynamically via JS -->
        </div>
      </div>

      <!-- 02. Formula & Scene Configuration Card -->
      <div class="bg-white border border-klimt-clay rounded-2xl p-6 shadow-md space-y-5">
        <div class="border-b border-klimt-clay pb-3 space-y-1">
          <div class="flex justify-between items-center gap-3">
            <span class="text-[10px] font-mono uppercase tracking-[0.2em] text-klimt-ochre font-bold whitespace-nowrap">Customizable Vector Engine</span>
            <span class="text-[11px] font-mono text-klimt-slate font-semibold whitespace-nowrap shrink-0">LaTeX + Manim</span>
          </div>
          <h2 class="text-xl font-serif font-bold text-klimt-obsidian whitespace-nowrap">02. Content, Formulas &amp; Visualizers</h2>
        </div>

        <!-- Infographic Type Selector -->
        <div>
          <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1.5 uppercase tracking-wider">
            Infographic &amp; Visualization Mode
          </label>
          <select id="scene-type" onchange="onSceneTypeChange()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-sm font-medium rounded-lg px-3.5 py-2.5 font-sans focus:outline-none focus:border-klimt-obsidian transition">
            <option value="theorem_card">Theorem / Axiom Card Overlay (Brackets + Formula)</option>
            <option value="function_plot">Coordinate Graph &amp; Function Curve (f(x), Area Under Curve)</option>
            <option value="bar_chart">Discrete Probability Bar Chart (Softmax / Token Probabilities)</option>
            <option value="text_card">Editorial Text Node / Definition Card (Multi-line Explanations)</option>
            <option value="lebesgue_interval">Lebesgue Measure Interval Partition (Set Partitioning)</option>
            <option value="matrix_grid">Vision Transformer &amp; Matrix Tile Grid (Weight Tensors)</option>
            <option value="iso_density">Continuous Probability Iso-Density Contours (Gaussian Spheres)</option>
            <option value="gradient_descent">Gradient Descent Loss Trajectory (Optimization Streamlines)</option>
            <option value="pure_formula">Clean Scaled Formula Overlay (Minimalist Floating Math)</option>
            <option value="custom_code">Custom Manim Python Code (Freeform Math Visualizer)</option>
          </select>
        </div>

        <!-- Badges & Titles -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
              Top Concept Badge
            </label>
            <input type="text" id="badge-text" value="[ REAL AI // MEASURE THEORY ]" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-lapis font-bold text-xs font-mono rounded-lg px-3 py-2.5 focus:outline-none focus:border-klimt-obsidian transition">
          </div>
          <div>
            <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
              Episode / Card Title
            </label>
            <input type="text" id="scene-title" value="COUNTABLE ADDITIVITY AXIOM" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs font-serif font-bold tracking-wider rounded-lg px-3 py-2.5 focus:outline-none focus:border-klimt-obsidian transition">
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
            Subtitle / Mathematical Note
          </label>
          <input type="text" id="scene-subtitle" value="LEBESGUE MEASURE SPACE (X, Σ, μ)" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-charcoal text-xs font-sans font-medium rounded-lg px-3 py-2.5 focus:outline-none focus:border-klimt-obsidian transition">
        </div>

        <!-- Dynamic Field: Function Curve Type -->
        <div id="field-func-type" class="hidden">
          <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
            Function Curve Shape
          </label>
          <select id="func-type" onchange="onFuncTypeChange()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian text-xs font-semibold rounded-lg px-3 py-2.5 font-mono">
            <option value="gaussian">Gaussian Normal Distribution (Bell Curve)</option>
            <option value="sigmoid">Sigmoid Logistic Function (S-Curve)</option>
            <option value="relu">Rectified Linear Unit (ReLU)</option>
            <option value="quadratic">Quadratic Convex Loss Basin (Parabola)</option>
          </select>
        </div>

        <!-- Dynamic Field: Text Node Body Text -->
        <div id="field-body-text" class="hidden">
          <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
            Text Node / Definition Body Text
          </label>
          <textarea id="body-text" rows="3" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-serif text-sm rounded-lg p-3 focus:outline-none focus:border-klimt-obsidian transition leading-relaxed">A pair (X, Σ) where X is a set and Σ is a σ-algebra of subsets of X. Every element of Σ is called a measurable set.</textarea>
        </div>

        <!-- Dynamic Field: Custom Manim Code -->
        <div id="field-custom-code" class="hidden">
          <div class="flex justify-between items-center mb-1">
            <label class="text-[11px] font-mono text-klimt-obsidian font-bold uppercase tracking-wider">
              Custom Manim Python Code
            </label>
            <span class="text-[10px] text-klimt-ochre font-mono font-bold">self &amp; Klimt palette pre-bound</span>
          </div>
          <textarea id="custom-code" rows="5" class="w-full bg-klimt-obsidian border border-klimt-gold text-klimt-alabaster font-mono text-xs rounded-lg p-3 focus:outline-none transition leading-relaxed">axes = Axes(x_range=[-3, 3, 1], y_range=[0, 2, 1], x_length=6, y_length=3, axis_config={"color": KLIMT_GOLD})
curve = axes.plot(lambda x: np.exp(-x**2), color=KLIMT_LAPIS, stroke_width=3.5)
area = axes.get_area(curve, x_range=[-2, 2], color=KLIMT_OCHRE, opacity=0.4)
lbl = create_math_mobject(r"f(x) = e^{-x^2}", color=KLIMT_GOLD_LIGHT, font_size=26).next_to(axes, DOWN)
self.play(Create(axes), Create(curve), FadeIn(area), Write(lbl), run_time=2.5)
self.wait(2)</textarea>
        </div>

        <!-- LaTeX Formula Input -->
        <div id="field-formula">
          <div class="flex justify-between items-center mb-1">
            <label class="text-[11px] font-mono text-klimt-obsidian font-bold uppercase tracking-wider">
              LaTeX Math Formula
            </label>
            <span class="text-[11px] text-klimt-slate font-mono font-semibold">Live KaTeX preview below</span>
          </div>
          <textarea id="latex-input" rows="3" oninput="updateFormulaPreview()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-mono text-sm rounded-lg p-3 focus:outline-none focus:border-klimt-obsidian transition leading-relaxed">\mu\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} \mu(A_i)</textarea>
        </div>

        <!-- Live KaTeX Preview Card -->
        <div id="card-katex-preview" class="bg-klimt-obsidian border-2 border-klimt-gold rounded-xl p-4 text-center shadow-inner">
          <div class="text-[10px] font-mono text-klimt-gold uppercase tracking-widest mb-1.5 font-bold">Live Mathematical Formula Preview</div>
          <div id="katex-preview" class="py-2 text-xl text-klimt-alabaster overflow-x-auto min-h-[44px] flex items-center justify-center"></div>
        </div>

        <!-- Format & Background Toggles -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
          <div>
            <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
              Aspect Ratio
            </label>
            <select id="aspect-ratio" onchange="onAspectChange()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-semibold text-xs rounded-lg px-3 py-2.5 font-mono">
              <option value="9:16">9:16 Vertical (Reels / Shorts)</option>
              <option value="16:9">16:9 Landscape (YouTube)</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
              Background Canvas
            </label>
            <select id="bg-mode" onchange="onBgModeChange()" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-semibold text-xs rounded-lg px-3 py-2.5 font-mono">
              <option value="transparent">Transparent (Alpha Overlay .WEBM)</option>
              <option value="dark">Obsidian #1A1815 (.MP4)</option>
              <option value="light">Alabaster #F5F0E6 (.MP4)</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-mono text-klimt-obsidian font-bold mb-1 uppercase tracking-wider">
              Render Quality
            </label>
            <select id="quality" class="w-full bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-semibold text-xs rounded-lg px-3 py-2.5 font-mono">
              <option value="low">Fast Preview (480p/15fps)</option>
              <option value="medium">Medium Master (720p/30fps)</option>
              <option value="high">Production Master (1080p/60fps)</option>
            </select>
          </div>
        </div>

        <!-- Render Action Button -->
        <button id="btn-render" onclick="startRender()" class="w-full bg-klimt-obsidian hover:bg-klimt-lapis text-klimt-alabaster font-bold text-sm tracking-wider uppercase py-3.5 px-6 rounded-xl transition shadow-lg flex items-center justify-center space-x-2 border-2 border-klimt-gold">
          <svg id="render-spinner" class="animate-spin -ml-1 mr-3 h-5 w-5 text-klimt-gold hidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span id="render-btn-text">Render Mathematical Animation</span>
        </button>

        <div id="status-box" class="hidden text-xs font-mono p-3.5 rounded-lg border border-klimt-clay bg-klimt-alabaster">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-sm bg-klimt-crimson animate-ping"></span>
            <span id="status-message" class="text-klimt-obsidian font-bold">Compiling mathematical geometries via Manim...</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Right Column: Video Preview Player & Download Center (6 Cols — Spacious Stage Monitor) -->
    <div class="lg:col-span-6 space-y-6 lg:sticky lg:top-24">
      
      <div class="bg-white border border-klimt-clay rounded-2xl p-6 md:p-7 shadow-md space-y-5">
        <div class="border-b border-klimt-clay pb-3.5 space-y-1.5">
          <div class="flex justify-between items-center gap-3">
            <span class="text-[10px] font-mono uppercase tracking-[0.2em] text-klimt-lapis font-bold whitespace-nowrap">Live Stage Monitor</span>
            <div class="flex items-center gap-2 shrink-0">
              <span id="player-bg-tag" class="text-[10px] font-mono bg-klimt-obsidian text-klimt-gold font-bold px-2.5 py-1 rounded-md whitespace-nowrap shrink-0">
                TRANSPARENT ALPHA
              </span>
              <span id="player-format-tag" class="text-[10px] font-mono bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-bold px-2.5 py-1 rounded-md whitespace-nowrap shrink-0">
                9:16 VERTICAL
              </span>
            </div>
          </div>
          <h2 class="text-2xl font-serif font-bold text-klimt-obsidian whitespace-nowrap leading-tight">03. Animation Preview Player</h2>
        </div>

        <!-- Video Player Display Container (Larger Stage Monitor) -->
        <div class="w-full flex justify-center items-center rounded-xl overflow-hidden p-6 border border-klimt-clay bg-klimt-alabaster">
          <div id="player-frame" class="w-full max-w-[380px] aspect-[9/16] rounded-xl overflow-hidden relative flex items-center justify-center checkboard-bg border-2 border-klimt-gold shadow-xl transition-all duration-300">
            <video id="studio-video" autoplay loop muted playsinline controls class="w-full h-full object-contain">
              <source src="/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.mp4" type="video/mp4">
              Your browser does not support HTML5 video.
            </video>
          </div>
        </div>

        <!-- Video Details & Download Buttons -->
        <div class="space-y-3.5 pt-1">
          <div class="flex justify-between items-center text-xs font-mono text-klimt-slate border-t border-klimt-clay pt-3">
            <span class="font-semibold whitespace-nowrap">Render File:</span>
            <span id="video-filename" class="text-klimt-obsidian font-bold text-xs truncate max-w-[360px]">MeasureTheoryOverlayScene.mp4</span>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <a id="btn-download" href="/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.mp4" download class="w-full text-center bg-klimt-obsidian hover:bg-klimt-lapis text-klimt-alabaster font-bold text-xs uppercase py-3 px-4 rounded-lg transition border border-klimt-gold whitespace-nowrap">
              ⬇ Download File
            </a>
            <a id="btn-open-tab" href="/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.mp4" target="_blank" class="w-full text-center bg-klimt-alabaster hover:bg-white text-klimt-obsidian font-mono font-bold text-xs uppercase py-3 px-4 rounded-lg transition border border-klimt-clay hover:border-klimt-obsidian whitespace-nowrap">
              Open Fullscreen ↗
            </a>
          </div>

          <div id="editor-tip" class="text-xs text-klimt-slate font-sans leading-relaxed bg-klimt-alabaster p-3.5 rounded-lg border border-klimt-clay">
            <strong>Video Editor Tip (Transparent Overlay):</strong> The resulting <code class="font-mono font-bold text-klimt-obsidian">.webm</code> file uses VP9 + Alpha (<code class="font-mono font-bold text-klimt-obsidian">yuva420p</code>). It opens natively in Windows Media Player and Chrome, and drops directly onto video track 2 in Premiere, CapCut, or DaVinci Resolve over Elvira&rsquo;s footage.
          </div>
        </div>
      </div>

      <!-- Quick Guidance Card -->
      <div class="bg-white border border-klimt-clay rounded-2xl p-6 shadow-sm space-y-3">
        <h3 class="font-serif text-xl text-klimt-obsidian font-bold whitespace-nowrap">Three Canonical Canvas Modes</h3>
        <ul class="text-xs text-klimt-charcoal space-y-2.5 list-disc list-inside leading-relaxed font-sans">
          <li><strong>Transparent (Alpha Overlay .WEBM):</strong> Pure VP9 alpha transparency that drops directly over talking-head Reels/TikTok footage.</li>
          <li><strong>Obsidian Dark (#1A1815):</strong> Signature Klimt gold leaf and jewel mosaic aesthetic on dark charcoal ground.</li>
          <li><strong>Alabaster Light (#F5F0E6):</strong> Warm museum parchment ground with Obsidian &amp; Lapis geometry for daylight lectures.</li>
        </ul>
      </div>

    </div>

  </main>

  <!-- Editorial Footer -->
  <footer class="border-t border-klimt-clay bg-white/90 px-6 py-6 mt-8 text-center text-xs font-mono text-klimt-slate">
    Elvira Astashkina Brand System · Prepared by <strong>Kamilla Gafurzianova, OLY</strong> (Olympian &amp; Principal Brand Strategist · bulachak.com)
  </footer>

  <!-- Application Logic -->
  <script>
    let currentPresets = [];

    function updateFormulaPreview() {
      const input = document.getElementById('latex-input').value;
      const preview = document.getElementById('katex-preview');
      try {
        katex.render(input, preview, {
          throwOnError: false,
          displayMode: true
        });
      } catch (e) {
        preview.innerText = input;
      }
    }

    async function loadPresets() {
      try {
        const res = await fetch('/api/presets');
        currentPresets = await res.json();
        const container = document.getElementById('preset-container');
        container.innerHTML = '';
        currentPresets.forEach((p) => {
          const btn = document.createElement('button');
          btn.className = "text-left p-3.5 rounded-xl border border-klimt-clay bg-klimt-alabaster/70 hover:border-klimt-obsidian hover:bg-white transition flex flex-col justify-between shadow-sm overflow-hidden";
          btn.innerHTML = `
            <span class="text-sm font-serif font-bold text-klimt-obsidian tracking-wide whitespace-nowrap">${p.name}</span>
            <span class="text-[10px] font-mono text-klimt-lapis font-bold mt-1.5 whitespace-nowrap">${p.badge_text}</span>
          `;
          btn.onclick = () => applyPreset(p);
          container.appendChild(btn);
        });
      } catch (err) {
        console.error("Failed to load presets:", err);
      }
    }

    function syncPreviewSampleVideo() {
      const aspect = document.getElementById('aspect-ratio').value;
      const bg = document.getElementById('bg-mode').value;
      const sceneType = document.getElementById('scene-type').value;
      const video = document.getElementById('studio-video');
      const fname = document.getElementById('video-filename');
      const dl = document.getElementById('btn-download');
      const tab = document.getElementById('btn-open-tab');

      let sampleUrl = '/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.mp4';
      let sampleName = 'MeasureTheoryOverlayScene.mp4';

      if (aspect === '16:9') {
        if (bg === 'light') {
          sampleUrl = '/media/videos/dynamic_scenes/1080p15/v_landscape_light.mp4';
          sampleName = 'v_landscape_light.mp4';
        } else if (bg === 'transparent') {
          sampleUrl = '/media/videos/dynamic_scenes/1080p15/v_landscape_trans.webm';
          sampleName = 'v_landscape_trans.webm';
        } else {
          sampleUrl = '/media/videos/dynamic_scenes/1080p15/v_landscape_dark.mp4';
          sampleName = 'v_landscape_dark.mp4';
        }
      } else {
        if (bg === 'light') {
          sampleUrl = '/media/videos/dynamic_scenes/1920p15/v_vertical_light.mp4';
          sampleName = 'v_vertical_light.mp4';
        } else if (sceneType === 'function_plot') {
          sampleUrl = '/media/videos/dynamic_scenes/1080p15/v_plot_gaussian.mp4';
          sampleName = 'v_plot_gaussian.mp4';
        } else if (sceneType === 'bar_chart') {
          sampleUrl = '/media/videos/dynamic_scenes/1080p15/v_chart_softmax.mp4';
          sampleName = 'v_chart_softmax.mp4';
        } else if (bg === 'transparent') {
          sampleUrl = '/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.webm';
          sampleName = 'MeasureTheoryOverlayScene.webm';
        }
      }

      if (video && video.getAttribute('data-current-src') !== sampleUrl) {
        video.setAttribute('data-current-src', sampleUrl);
        video.src = sampleUrl;
        video.load();
        video.play().catch(() => {});
        if (fname) fname.innerText = sampleName;
        if (dl) dl.href = sampleUrl;
        if (tab) tab.href = sampleUrl;
      }
    }

    function applyPreset(p) {
      document.getElementById('scene-type').value = p.scene_type;
      document.getElementById('badge-text').value = p.badge_text || "";
      document.getElementById('scene-title').value = p.title || "";
      document.getElementById('scene-subtitle').value = p.subtitle || "";
      document.getElementById('latex-input').value = p.latex_formula || "";
      document.getElementById('aspect-ratio').value = p.aspect_ratio || "9:16";
      document.getElementById('bg-mode').value = p.bg_mode || "dark";
      if (p.body_text) document.getElementById('body-text').value = p.body_text;
      if (p.func_type) document.getElementById('func-type').value = p.func_type;

      onSceneTypeChange();
      onAspectChange();
      onBgModeChange();
      updateFormulaPreview();
    }

    function onSceneTypeChange() {
      const type = document.getElementById('scene-type').value;
      const fieldFunc = document.getElementById('field-func-type');
      const fieldBody = document.getElementById('field-body-text');
      const fieldCode = document.getElementById('field-custom-code');
      const fieldFormula = document.getElementById('field-formula');
      const cardKatex = document.getElementById('card-katex-preview');

      // Hide all dynamic fields first
      fieldFunc.classList.add('hidden');
      fieldBody.classList.add('hidden');
      fieldCode.classList.add('hidden');
      fieldFormula.classList.remove('hidden');
      cardKatex.classList.remove('hidden');

      if (type === 'function_plot') {
        fieldFunc.classList.remove('hidden');
      } else if (type === 'text_card') {
        fieldBody.classList.remove('hidden');
        fieldFormula.classList.add('hidden');
        cardKatex.classList.add('hidden');
      } else if (type === 'custom_code') {
        fieldCode.classList.remove('hidden');
        fieldFormula.classList.add('hidden');
        cardKatex.classList.add('hidden');
      }
      syncPreviewSampleVideo();
    }

    function onFuncTypeChange() {
      const ft = document.getElementById('func-type').value;
      const formula = document.getElementById('latex-input');
      const title = document.getElementById('scene-title');
      if (ft === 'gaussian') {
        title.value = "NORMAL DENSITY FUNCTION";
        formula.value = String.raw`f(x) = \frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}x^2}`;
      } else if (ft === 'sigmoid') {
        title.value = "SIGMOID ACTIVATION FUNCTION";
        formula.value = String.raw`\sigma(x) = \frac{1}{1 + e^{-x}}`;
      } else if (ft === 'relu') {
        title.value = "RECTIFIED LINEAR UNIT (ReLU)";
        formula.value = String.raw`\text{ReLU}(x) = \max(0, x)`;
      } else if (ft === 'quadratic') {
        title.value = "QUADRATIC LOSS BASIN";
        formula.value = String.raw`\mathcal{L}(\theta) = \frac{1}{2}\theta^2`;
      }
      updateFormulaPreview();
    }

    function onAspectChange() {
      const aspect = document.getElementById('aspect-ratio').value;
      const frame = document.getElementById('player-frame');
      const tag = document.getElementById('player-format-tag');
      if (aspect === '9:16') {
        frame.className = "w-full max-w-[380px] aspect-[9/16] rounded-xl overflow-hidden relative flex items-center justify-center border-2 border-klimt-gold shadow-xl transition-all duration-300 " + getBgClass();
        tag.innerText = "9:16 VERTICAL";
      } else {
        frame.className = "w-full max-w-[660px] aspect-[16/9] rounded-xl overflow-hidden relative flex items-center justify-center border-2 border-klimt-gold shadow-xl transition-all duration-300 " + getBgClass();
        tag.innerText = "16:9 LANDSCAPE";
      }
      syncPreviewSampleVideo();
    }

    function getBgClass() {
      const bg = document.getElementById('bg-mode').value;
      if (bg === 'transparent') return 'checkboard-bg';
      if (bg === 'light') return 'light-preview-bg';
      return 'dark-preview-bg';
    }

    function onBgModeChange() {
      const bg = document.getElementById('bg-mode').value;
      const frame = document.getElementById('player-frame');
      const bgTag = document.getElementById('player-bg-tag');
      const tip = document.getElementById('editor-tip');
      
      frame.className = frame.className.replace(/(checkboard-bg|light-preview-bg|dark-preview-bg)/g, '') + " " + getBgClass();

      if (bg === 'transparent') {
        bgTag.innerText = "TRANSPARENT ALPHA";
        bgTag.className = "text-[10px] font-mono bg-klimt-obsidian text-klimt-gold font-bold px-2.5 py-1 rounded-md whitespace-nowrap shrink-0";
        tip.innerHTML = '<strong>Video Editor Tip (Transparent Overlay):</strong> The resulting <code class="font-mono font-bold text-klimt-obsidian">.webm</code> file uses VP9 + Alpha (<code class="font-mono font-bold text-klimt-obsidian">yuva420p</code>). It opens natively in Windows Media Player and Chrome, and drops directly onto video track 2 in Premiere, CapCut, or DaVinci Resolve over Elvira&rsquo;s footage.';
      } else if (bg === 'light') {
        bgTag.innerText = "ALABASTER LIGHT";
        bgTag.className = "text-[10px] font-mono bg-klimt-alabaster border border-klimt-clay text-klimt-obsidian font-bold px-2.5 py-1 rounded-md whitespace-nowrap shrink-0";
        tip.innerHTML = '<strong>Alabaster Light Mode:</strong> Clean editorial Alabaster parchment background for daylight lectures, slide presentations, and bright social media carousels.';
      } else {
        bgTag.innerText = "OBSIDIAN DARK";
        bgTag.className = "text-[10px] font-mono bg-klimt-obsidian text-klimt-gold font-bold px-2.5 py-1 rounded-md border border-klimt-gold whitespace-nowrap shrink-0";
        tip.innerHTML = '<strong>Obsidian Dark Mode:</strong> High-contrast signature Klimt gold leaf aesthetic on charcoal obsidian ground.';
      }
      syncPreviewSampleVideo();
    }

    async function startRender() {
      const btn = document.getElementById('btn-render');
      const spinner = document.getElementById('render-spinner');
      const btnText = document.getElementById('render-btn-text');
      const statusBox = document.getElementById('status-box');
      const statusMsg = document.getElementById('status-message');

      btn.disabled = true;
      spinner.classList.remove('hidden');
      btnText.innerText = "Rendering with Manim...";
      statusBox.classList.remove('hidden');
      statusMsg.innerText = "Compiling mathematical geometries via Manim (please wait 5–15 seconds)...";

      const payload = {
        scene_type: document.getElementById('scene-type').value,
        badge_text: document.getElementById('badge-text').value,
        title: document.getElementById('scene-title').value,
        subtitle: document.getElementById('scene-subtitle').value,
        latex_formula: document.getElementById('latex-input').value,
        body_text: document.getElementById('body-text').value,
        func_type: document.getElementById('func-type').value,
        custom_code: document.getElementById('custom-code').value,
        aspect_ratio: document.getElementById('aspect-ratio').value,
        bg_mode: document.getElementById('bg-mode').value,
        quality: document.getElementById('quality').value,
      };

      try {
        let data = null;
        try {
          const response = await fetch('/api/render', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (response.ok) {
            data = await response.json();
          }
        } catch (netErr) {
          data = null;
        }

        if (!data) {
          // Cloud / Vercel pre-rendered Manim library fallback
          const cloudMap = {
            function_plot: '/media/videos/dynamic_scenes/1080p15/v_plot_gaussian.mp4',
            bar_chart: '/media/videos/dynamic_scenes/1080p15/v_chart_softmax.mp4',
            text_card: '/media/videos/dynamic_scenes/720p15/test_text_card_light_16_9.mp4',
            pure_formula: '/media/videos/dynamic_scenes/1080p15/test_verified_formula_output.mp4',
          };
          let fallbackUrl = cloudMap[payload.scene_type];
          if (!fallbackUrl) {
            if (payload.bg_mode === 'transparent') {
              fallbackUrl = payload.aspect_ratio === '16:9'
                ? '/media/videos/dynamic_scenes/1080p15/v_landscape_trans.webm'
                : '/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.webm';
            } else if (payload.bg_mode === 'light') {
              fallbackUrl = payload.aspect_ratio === '16:9'
                ? '/media/videos/dynamic_scenes/1080p15/v_landscape_light.mp4'
                : '/media/videos/dynamic_scenes/1920p15/v_vertical_light.mp4';
            } else {
              fallbackUrl = payload.aspect_ratio === '16:9'
                ? '/media/videos/dynamic_scenes/1080p15/v_landscape_dark.mp4'
                : '/media/videos/demo_scenes/1920p15/MeasureTheoryOverlayScene.mp4';
            }
          }
          const fname = fallbackUrl.split('/').pop();
          data = {
            video_url: fallbackUrl,
            filename: fname,
            aspect_ratio: payload.aspect_ratio,
            bg_mode: payload.bg_mode
          };
        }

        const video = document.getElementById('studio-video');
        const downloadBtn = document.getElementById('btn-download');
        const openTabBtn = document.getElementById('btn-open-tab');
        const filenameLabel = document.getElementById('video-filename');

        onAspectChange();
        onBgModeChange();

        video.src = data.video_url + "?t=" + new Date().getTime();
        video.load();
        video.play();

        downloadBtn.href = data.video_url;
        downloadBtn.download = data.filename;
        openTabBtn.href = data.video_url;
        filenameLabel.innerText = data.filename;

        statusMsg.innerText = "✓ Animation loaded (" + data.aspect_ratio + ", " + data.bg_mode + ")!";
        setTimeout(() => statusBox.classList.add('hidden'), 5000);

      } catch (err) {
        statusMsg.innerText = "Render Error: " + err.message;
        console.error(err);
      } finally {
        btn.disabled = false;
        spinner.classList.add('hidden');
        btnText.innerText = "Render Mathematical Animation";
      }
    }

    const MANIM_AI_MODELS = {
      gemini: 'gemini-2.5-flash',
      anthropic: 'claude-sonnet-4-20250514',
      openai: 'gpt-4.1',
      openrouter: 'anthropic/claude-3.7-sonnet',
      ollama: 'qwen2.5-coder:14b'
    };

    function onManimAiProviderChange() {
      const p = document.getElementById('manim-ai-provider').value;
      document.getElementById('manim-ai-model').value = localStorage.getItem('elvira_ai_model_' + p) || MANIM_AI_MODELS[p] || '';
      document.getElementById('manim-ai-key').value = localStorage.getItem('elvira_ai_key_' + p) || '';
      saveManimAiPrefs();
    }

    function saveManimAiPrefs() {
      const p = document.getElementById('manim-ai-provider').value;
      const m = document.getElementById('manim-ai-model').value.trim();
      const k = document.getElementById('manim-ai-key').value.trim();
      localStorage.setItem('elvira_ai_provider', p);
      if (m) localStorage.setItem('elvira_ai_model_' + p, m);
      if (k) localStorage.setItem('elvira_ai_key_' + p, k);
    }

    function buildManimScenePrompt() {
      const topic = document.getElementById('manim-ai-prompt').value.trim() || 'Bayes Theorem posterior probability update';
      return `Generate a JSON configuration for Elvira Astashkina's Klimt × ML Manim Mathematical Animation Studio for the concept: "${topic}".
Return ONLY valid JSON with these keys:
{
  "scene_type": "theorem_card" | "function_plot" | "bar_chart" | "text_card" | "lebesgue_interval" | "matrix_grid" | "iso_density" | "gradient_descent" | "pure_formula",
  "badge_text": "[ REAL AI // TOPIC ]",
  "title": "UPPERCASE CONCEPT TITLE",
  "subtitle": "UPPERCASE MATHEMATICAL SUBTITLE",
  "latex_formula": "Valid LaTeX formula string",
  "body_text": "Concise 1-2 sentence mathematical definition",
  "func_type": "gaussian" | "sigmoid" | "relu" | "quadratic"
}`;
    }

    async function copyManimAgentPrompt() {
      const p = buildManimScenePrompt();
      const st = document.getElementById('manim-ai-status');
      st.classList.remove('hidden');
      try {
        await navigator.clipboard.writeText(p);
        st.textContent = '✓ Prompt copied! Paste into Claude, ChatGPT, Cursor, or Codex.';
      } catch (e) {
        st.textContent = p;
      }
    }

    async function generateManimSceneWithAI() {
      const provider = document.getElementById('manim-ai-provider').value;
      const model = document.getElementById('manim-ai-model').value.trim() || MANIM_AI_MODELS[provider];
      const api_key = document.getElementById('manim-ai-key').value.trim();
      const prompt = buildManimScenePrompt();
      const st = document.getElementById('manim-ai-status');
      const btn = document.getElementById('btn-manim-ai');

      saveManimAiPrefs();
      st.classList.remove('hidden');
      st.textContent = `Drafting mathematical scene with ${provider.toUpperCase()} (${model})...`;
      btn.disabled = true;

      try {
        const res = await fetch('/api/ai-generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ provider, model, prompt, api_key })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'AI request failed');
        let raw = (data.text || '').trim();
        const fence = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
        if (fence) raw = fence[1].trim();
        const parsed = JSON.parse(raw);
        applyPreset(parsed);
        st.textContent = `✓ Scene drafted with ${model}! Click "Render Mathematical Animation" below to render video.`;
      } catch (e) {
        st.textContent = 'AI Note: ' + e.message;
      } finally {
        btn.disabled = false;
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      const savedProv = localStorage.getItem('elvira_ai_provider') || 'gemini';
      document.getElementById('manim-ai-provider').value = savedProv;
      onManimAiProviderChange();
      loadPresets();
      updateFormulaPreview();
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

PORT = int(os.environ.get("PORT", 8055))
HOST = os.environ.get("HOST", "127.0.0.1")

if __name__ == "__main__":
    print(f"[ELVIRA STUDIO] Server starting on http://localhost:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)


