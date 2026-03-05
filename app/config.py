from pathlib import Path

BASE_DIR = Path.home() / "Pictures" / "photobooth"

SESSIONS_DIR = BASE_DIR / "sessions"
FRAMES_DIR = BASE_DIR / "frames"
OUTPUT_DIR = BASE_DIR / "output"
DB_DIR = BASE_DIR / "database"

DOMAIN = "https://pb.nakrub.me"

PRINTER_NAME = "Canon_SELPHY_CP1500"

DEFAULT_PHOTO_COUNT = 6


def init_directories():
    for p in [SESSIONS_DIR, FRAMES_DIR, OUTPUT_DIR, DB_DIR]:
        p.mkdir(parents=True, exist_ok=True)