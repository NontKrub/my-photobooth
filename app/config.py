import os
from pathlib import Path

BASE_DIR = Path.home() / "Pictures" / "photobooth"

SESSIONS_DIR = BASE_DIR / "sessions"
FRAMES_DIR = BASE_DIR / "frames"
OUTPUT_DIR = BASE_DIR / "output"
DB_DIR = BASE_DIR / "database"

# Drop JPG files here to simulate camera input during local testing.
INPUT_DIR = BASE_DIR / "input"

DOMAIN = "https://pb.nakrub.me"

PRINTER_NAME = "Canon_SELPHY_CP1500"

DEFAULT_PHOTO_COUNT = 6

# Set MOCK_PRINTER=1 to skip actual printing (useful when no printer is connected).
MOCK_PRINTER = os.environ.get("MOCK_PRINTER", "0") == "1"


def init_directories():
    for p in [SESSIONS_DIR, FRAMES_DIR, OUTPUT_DIR, DB_DIR, INPUT_DIR]:
        p.mkdir(parents=True, exist_ok=True)