"""
settings.py – application-wide configuration for the PhotoBooth backend.
"""

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
STORAGE_DIR = BASE_DIR / "storage" / "photos"
DB_PATH = BASE_DIR / "storage" / "photobooth.db"
FRAMES_DIR = BASE_DIR / "storage" / "frames"

# ── Camera ─────────────────────────────────────────────────────────────────
# Maximum number of OpenCV camera indices to probe
MAX_OPENCV_INDEX = 5

# ── Session defaults ────────────────────────────────────────────────────────
DEFAULT_LAYOUT = "2x2"       # "2x2" | "3x2" | "1x3" | "2x1"
DEFAULT_PHOTO_COUNT = 4

# ── Collage canvas ──────────────────────────────────────────────────────────
CANVAS_WIDTH = 1800
CANVAS_HEIGHT = 1200
CANVAS_PADDING = 20

# ── Preview stream ──────────────────────────────────────────────────────────
PREVIEW_FPS = 30
PREVIEW_JPEG_QUALITY = 80

# ── Printer ─────────────────────────────────────────────────────────────────
PRINTER_NAME = "Canon_SELPHY_CP1500"

import os

# ── QR / sharing ─────────────────────────────────────────────────────────────
# Override via the PHOTOBOOTH_DOMAIN environment variable when deploying.
DOMAIN = os.getenv("PHOTOBOOTH_DOMAIN", "http://localhost:8000")


def ensure_dirs() -> None:
    """Create required directories if they don't exist."""
    for d in (STORAGE_DIR, FRAMES_DIR, DB_PATH.parent):
        d.mkdir(parents=True, exist_ok=True)
