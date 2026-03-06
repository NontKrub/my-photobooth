"""
main.py – FastAPI backend for the PhotoBooth application.

Endpoints
---------
GET  /list-cameras       Detect all connected cameras
POST /select-camera      Choose which camera to use
POST /start-session      Create a new session
POST /start-preview      Start MJPEG preview stream
GET  /preview-stream     MJPEG stream (use in <img> tag)
DELETE /stop-preview     Stop the preview stream
POST /capture            Capture one photo in the active session
POST /process            Generate the collage for a session
GET  /result/{id}        Retrieve session result
GET  /sessions           List all saved sessions
"""

import asyncio
import logging
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from camera_manager import camera_manager
from capture_service import CaptureService
from database import get_all_sessions, get_session, init_db, save_session
from image_processor import compose_collage
from session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="PhotoBooth API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage path (relative to this file: ../storage/photos)
STORAGE_DIR = Path(__file__).parent.parent / "storage" / "photos"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/photos", StaticFiles(directory=str(STORAGE_DIR)), name="photos")

# Service instances
_capture_service = CaptureService(camera_manager)
_active_session: Optional[SessionManager] = None


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def _startup() -> None:
    init_db()
    logger.info("PhotoBooth API started")


@app.on_event("shutdown")
async def _shutdown() -> None:
    camera_manager.cleanup()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class SelectCameraRequest(BaseModel):
    camera_id: str


class StartSessionRequest(BaseModel):
    layout: str = "2x2"  # "2x2" | "3x2" | "1x3" | "2x1"
    photo_count: int = 4


class ProcessRequest(BaseModel):
    session_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/list-cameras")
async def list_cameras():
    """Detect and return all connected cameras."""
    cameras = await asyncio.get_event_loop().run_in_executor(
        None, camera_manager.detect_cameras
    )
    return {"cameras": cameras, "count": len(cameras)}


@app.post("/select-camera")
async def select_camera_endpoint(req: SelectCameraRequest):
    """Select a camera by its ID."""
    ok = await asyncio.get_event_loop().run_in_executor(
        None, camera_manager.select_camera, req.camera_id
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"status": "selected", "camera_id": req.camera_id}


@app.post("/start-session")
async def start_session(req: StartSessionRequest):
    """Create a new photobooth session."""
    global _active_session
    session_id = uuid.uuid4().hex[:8]
    session_dir = STORAGE_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    _active_session = SessionManager(
        session_id=session_id,
        session_dir=session_dir,
        layout=req.layout,
        photo_count=req.photo_count,
    )
    logger.info("New session: %s layout=%s photos=%d", session_id, req.layout, req.photo_count)
    return {
        "session_id": session_id,
        "layout": req.layout,
        "photo_count": req.photo_count,
    }


@app.post("/start-preview")
async def start_preview_endpoint():
    """Start the camera preview background thread."""
    if not camera_manager.get_selected_camera():
        raise HTTPException(status_code=400, detail="No camera selected")
    ok = await asyncio.get_event_loop().run_in_executor(
        None, camera_manager.start_preview
    )
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to start preview")
    return {"status": "preview_started"}


@app.get("/preview-stream")
async def preview_stream():
    """
    MJPEG stream for the camera preview.
    Use as the ``src`` of an ``<img>`` element.
    """

    def _generate():
        import time

        while camera_manager.is_preview_active():
            frame = camera_manager.get_current_frame()
            if frame:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            time.sleep(0.033)

    return StreamingResponse(
        _generate(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.delete("/stop-preview")
async def stop_preview_endpoint():
    """Stop the preview stream and release the camera."""
    camera_manager.stop_preview()
    return {"status": "preview_stopped"}


@app.post("/capture")
async def capture_photo():
    """Capture one photo and add it to the active session."""
    global _active_session
    if not _active_session:
        raise HTTPException(status_code=400, detail="No active session")
    if not _capture_service.begin_capture():
        raise HTTPException(status_code=409, detail="Capture already in progress")
    try:
        photo_num = len(_active_session.photos) + 1
        output_path = _active_session.session_dir / f"photo_{photo_num}.jpg"
        ok = await asyncio.get_event_loop().run_in_executor(
            None, camera_manager.capture_image, output_path
        )
        if not ok:
            raise HTTPException(status_code=500, detail="Capture failed")
        _active_session.add_photo(output_path)
        return {
            "photo_num": photo_num,
            "url": f"/photos/{_active_session.session_id}/photo_{photo_num}.jpg",
            "total": len(_active_session.photos),
            "complete": _active_session.is_complete(),
        }
    finally:
        _capture_service.end_capture()


@app.post("/process")
async def process_session(req: ProcessRequest):
    """Generate the collage for the active session."""
    global _active_session
    if not _active_session:
        raise HTTPException(status_code=400, detail="No active session")
    if _active_session.session_id != req.session_id:
        raise HTTPException(status_code=400, detail="Session ID mismatch")

    collage_path = _active_session.session_dir / "collage.jpg"
    ok = await asyncio.get_event_loop().run_in_executor(
        None,
        compose_collage,
        _active_session.photos,
        collage_path,
        _active_session.layout,
    )
    if not ok:
        raise HTTPException(status_code=500, detail="Collage generation failed")

    _active_session.collage_path = collage_path

    # Persist metadata
    save_session(
        session_id=_active_session.session_id,
        photo_count=len(_active_session.photos),
        layout=_active_session.layout,
        collage_path=str(collage_path),
    )

    return {
        "session_id": _active_session.session_id,
        "collage": f"/photos/{_active_session.session_id}/collage.jpg",
        "photos": _active_session.photo_urls(),
    }


@app.get("/result/{session_id}")
async def get_result(session_id: str):
    """Return photo and collage URLs for a given session."""
    session_dir = STORAGE_DIR / session_id
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    photos = sorted(session_dir.glob("photo_*.jpg"))
    collage = session_dir / "collage.jpg"
    return {
        "session_id": session_id,
        "photos": [f"/photos/{session_id}/{p.name}" for p in photos],
        "collage": f"/photos/{session_id}/collage.jpg" if collage.exists() else None,
    }


@app.get("/sessions")
async def list_sessions():
    """List all completed sessions stored in the database."""
    return {"sessions": get_all_sessions()}
