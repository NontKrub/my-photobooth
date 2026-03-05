import time
from pathlib import Path
from config import SESSIONS_DIR
from services.image_processor import compose_layout
from services.printer_service import print_photo
from services.qr_service import create_qr


class SessionManager:

    def __init__(self, photo_target):

        self.photo_target = photo_target

        ts = time.strftime("%Y%m%d_%H%M%S")

        self.session_dir = SESSIONS_DIR / ts

        self.session_dir.mkdir(parents=True)

        self.photos = []

    def add_photo(self, path):

        self.photos.append(path)

    def is_complete(self):

        return len(self.photos) >= self.photo_target

    def process_session(self):

        output = self.session_dir / "final.jpg"

        compose_layout(self.photos, output)

        print_photo(output)

        create_qr(output)