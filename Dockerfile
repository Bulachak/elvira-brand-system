FROM python:3.11-slim

# System dependencies for Manim Community, Cairo, Pango, LaTeX & FFmpeg (VP9 Alpha WebM + H.264 MP4)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-science \
    dvisvgm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV HOST=0.0.0.0
ENV PORT=8055
EXPOSE 8055

CMD ["python", "studio.py"]
