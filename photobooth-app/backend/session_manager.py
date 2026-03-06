"""
session_manager.py – tracks photos for a single photobooth session.
"""

from pathlib import Path
from typing import List, Optional


class SessionManager:
    """Holds state for one photobooth session."""

    def __init__(
        self,
        session_id: str,
        session_dir: Path,
        layout: str,
        photo_count: int,
    ) -> None:
        self.session_id = session_id
        self.session_dir = session_dir
        self.layout = layout
        self.photo_count = photo_count
        self.photos: List[Path] = []
        self.collage_path: Optional[Path] = None

    def add_photo(self, path: Path) -> None:
        self.photos.append(path)

    def is_complete(self) -> bool:
        return len(self.photos) >= self.photo_count

    def photo_urls(self, base_url: str = "/photos") -> List[str]:
        return [
            f"{base_url}/{self.session_id}/{p.name}" for p in self.photos
        ]
