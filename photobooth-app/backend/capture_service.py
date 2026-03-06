"""
capture_service.py – guards against concurrent capture requests.
"""

import threading
import logging

logger = logging.getLogger(__name__)


class CaptureService:
    """Thread-safe helper that prevents overlapping capture calls."""

    def __init__(self, camera_manager) -> None:
        self._camera_manager = camera_manager
        self._capturing = False
        self._lock = threading.Lock()

    def is_capturing(self) -> bool:
        with self._lock:
            return self._capturing

    def begin_capture(self) -> bool:
        """Mark a capture as in-progress. Returns False if already capturing."""
        with self._lock:
            if self._capturing:
                return False
            self._capturing = True
            return True

    def end_capture(self) -> None:
        with self._lock:
            self._capturing = False
