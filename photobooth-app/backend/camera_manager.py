"""
camera_manager.py – detects, selects, previews, and captures from cameras.

Supported cameras:
  - Built-in / USB webcams via OpenCV
  - Sony ZV-E10 (and any gphoto2-compatible camera) via gphoto2
"""

import logging
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import cv2

logger = logging.getLogger(__name__)


class CameraManager:
    """Thread-safe manager for camera detection, preview, and capture."""

    OPENCV_TYPE = "opencv"
    GPHOTO2_TYPE = "gphoto2"

    def __init__(self) -> None:
        self._selected: Optional[Dict[str, Any]] = None
        self._cap: Optional[cv2.VideoCapture] = None
        self._preview_active = False
        self._preview_thread: Optional[threading.Thread] = None
        self._current_frame: Optional[bytes] = None
        self._capture_lock = threading.Lock()
        self._frame_lock = threading.RLock()

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------

    def detect_cameras(self) -> List[Dict[str, Any]]:
        """Return a list of all detected cameras (OpenCV + gphoto2)."""
        cameras: List[Dict[str, Any]] = []
        cameras.extend(self._detect_opencv())
        cameras.extend(self._detect_gphoto2())
        return cameras

    def _detect_opencv(self) -> List[Dict[str, Any]]:
        cameras: List[Dict[str, Any]] = []
        for idx in range(5):
            cap = cv2.VideoCapture(idx)
            if not cap.isOpened():
                cap.release()
                continue
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            backend = cap.getBackendName()
            cap.release()
            name = "Built-in / Primary Camera" if idx == 0 else f"USB Camera {idx}"
            cameras.append(
                {
                    "id": f"opencv_{idx}",
                    "name": name,
                    "type": self.OPENCV_TYPE,
                    "index": idx,
                    "resolution": f"{w}x{h}",
                    "backend": backend,
                }
            )
        return cameras

    def _detect_gphoto2(self) -> List[Dict[str, Any]]:
        cameras: List[Dict[str, Any]] = []
        try:
            result = subprocess.run(
                ["gphoto2", "--auto-detect"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                return cameras
            for line in result.stdout.strip().splitlines()[2:]:
                line = line.strip()
                if not line or line.startswith("-"):
                    continue
                parts = line.rsplit(None, 1)
                if len(parts) < 2:
                    continue
                name, port = parts[0].strip(), parts[1].strip()
                cameras.append(
                    {
                        "id": f"gphoto2_{port.replace('/', '_')}",
                        "name": name,
                        "type": self.GPHOTO2_TYPE,
                        "port": port,
                        "resolution": "N/A",
                    }
                )
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            logger.warning("gphoto2 unavailable: %s", exc)
        return cameras

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def select_camera(self, camera_id: str) -> bool:
        """Select a camera by its ID. Returns True on success."""
        for cam in self.detect_cameras():
            if cam["id"] == camera_id:
                self._selected = cam
                logger.info("Selected camera: %s", cam["name"])
                return True
        return False

    def get_selected_camera(self) -> Optional[Dict[str, Any]]:
        return self._selected

    # ------------------------------------------------------------------
    # Preview
    # ------------------------------------------------------------------

    def start_preview(self) -> bool:
        """Start a background thread that continuously captures preview frames."""
        if self._preview_active:
            return True
        if not self._selected:
            logger.warning("No camera selected")
            return False
        if self._selected["type"] == self.OPENCV_TYPE:
            return self._start_opencv_preview()
        if self._selected["type"] == self.GPHOTO2_TYPE:
            return self._start_gphoto2_preview()
        return False

    def _start_opencv_preview(self) -> bool:
        idx = self._selected["index"]  # type: ignore[index]
        self._cap = cv2.VideoCapture(idx)
        if not self._cap.isOpened():
            logger.error("Cannot open camera %d", idx)
            return False
        self._preview_active = True
        self._preview_thread = threading.Thread(
            target=self._opencv_loop, daemon=True
        )
        self._preview_thread.start()
        return True

    def _opencv_loop(self) -> None:
        while self._preview_active:
            if self._cap is None or not self._cap.isOpened():
                logger.error("Camera disconnected during preview")
                self._preview_active = False
                break
            ret, frame = self._cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # mirror
                _, buf = cv2.imencode(
                    ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80]
                )
                with self._frame_lock:
                    self._current_frame = buf.tobytes()
            else:
                time.sleep(0.1)
            time.sleep(0.033)  # ~30 fps

    def _start_gphoto2_preview(self) -> bool:
        self._preview_active = True
        self._preview_thread = threading.Thread(
            target=self._gphoto2_loop, daemon=True
        )
        self._preview_thread.start()
        return True

    def _gphoto2_loop(self) -> None:
        while self._preview_active:
            try:
                result = subprocess.run(
                    ["gphoto2", "--capture-preview", "--stdout"],
                    capture_output=True,
                    timeout=5,
                )
                if result.returncode == 0 and result.stdout:
                    with self._frame_lock:
                        self._current_frame = result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
                logger.warning("gphoto2 preview error: %s", exc)
            time.sleep(0.1)

    def stop_preview(self) -> None:
        """Stop the preview thread and release the camera."""
        self._preview_active = False
        if self._preview_thread:
            self._preview_thread.join(timeout=2)
            self._preview_thread = None
        if self._cap:
            self._cap.release()
            self._cap = None
        with self._frame_lock:
            self._current_frame = None

    def get_current_frame(self) -> Optional[bytes]:
        """Return the latest JPEG preview frame, or None."""
        with self._frame_lock:
            return self._current_frame

    def is_preview_active(self) -> bool:
        return self._preview_active

    # ------------------------------------------------------------------
    # Capture
    # ------------------------------------------------------------------

    def capture_image(self, output_path: Path) -> bool:
        """Capture a still image and save it to *output_path*."""
        with self._capture_lock:
            if not self._selected:
                logger.error("No camera selected for capture")
                return False
            cam_type = self._selected["type"]
            if cam_type == self.OPENCV_TYPE:
                return self._capture_opencv(output_path)
            if cam_type == self.GPHOTO2_TYPE:
                return self._capture_gphoto2(output_path)
            return False

    def _capture_opencv(self, output_path: Path) -> bool:
        cap = self._cap
        owned = False
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(self._selected["index"])  # type: ignore[index]
            owned = True
        if not cap.isOpened():
            logger.error("Cannot open camera for capture")
            if owned:
                cap.release()
            return False
        # Drain stale frames so the captured shot is current
        for _ in range(5):
            cap.read()
        ret, frame = cap.read()
        if owned:
            cap.release()
        if not ret:
            logger.error("Failed to read capture frame")
            return False
        frame = cv2.flip(frame, 1)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), frame)
        logger.info("Captured: %s", output_path)
        return True

    def _capture_gphoto2(self, output_path: Path) -> bool:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        port = self._selected.get("port", "")  # type: ignore[union-attr]
        cmd = ["gphoto2"]
        if port:
            cmd += ["--port", port]
        cmd += ["--capture-image-and-download", "--filename", str(output_path)]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                logger.info("Captured via gphoto2: %s", output_path)
                return True
            logger.error("gphoto2 capture failed: %s", result.stderr)
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            logger.error("gphoto2 capture error: %s", exc)
            return False

    def cleanup(self) -> None:
        """Release all resources."""
        self.stop_preview()


# ---------------------------------------------------------------------------
# Module-level singleton + convenience functions
# ---------------------------------------------------------------------------

camera_manager = CameraManager()


def detect_cameras() -> List[Dict[str, Any]]:
    return camera_manager.detect_cameras()


def select_camera(camera_id: str) -> bool:
    return camera_manager.select_camera(camera_id)


def start_preview() -> bool:
    return camera_manager.start_preview()


def capture_image(output_path: Path) -> bool:
    return camera_manager.capture_image(output_path)
