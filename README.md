## PhotoBooth App

A full-stack photobooth application with a Python/FastAPI backend and a React
frontend.  Supports built-in webcams, USB cameras via OpenCV, and Sony ZV-E10
(or any gphoto2-compatible camera) via gphoto2.

---

### Project structure

```
photobooth-app/
├── backend/
│   ├── main.py            # FastAPI application & API endpoints
│   ├── camera_manager.py  # Camera detection, preview & capture
│   ├── capture_service.py # Concurrent-capture guard
│   ├── image_processor.py # Collage generation & image utilities
│   ├── session_manager.py # Per-session state
│   └── database.py        # SQLite persistence
├── frontend/              # React (Vite) UI
│   └── src/
│       ├── pages/         # IdlePage, CameraSelectPage, LayoutPage, PreviewPage, ResultPage
│       ├── components/    # CameraPreview, Countdown, LayoutSelector, ResultView
│       └── services/api.js
├── storage/
│   └── photos/            # Saved sessions  (<session_id>/photo_N.jpg + collage.jpg)
└── config/
    └── settings.py        # Application-wide settings
```

---

### Photobooth workflow

```
Idle screen → Select camera → Choose layout → Live preview
→ Countdown → Capture × N → Generate collage → Display result → Reset
```

---

### Supported cameras

| Camera | Driver |
|---|---|
| iMac FaceTime HD / built-in | OpenCV (index 0) |
| USB webcam | OpenCV (index 1+) |
| Sony ZV-E10 | gphoto2 |

---

### API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/list-cameras` | Detect all connected cameras |
| POST | `/select-camera` | Select a camera by ID |
| POST | `/start-session` | Create a new session |
| POST | `/start-preview` | Start MJPEG preview thread |
| GET | `/preview-stream` | MJPEG stream (use as `<img src>`) |
| DELETE | `/stop-preview` | Stop the preview thread |
| POST | `/capture` | Capture one photo |
| POST | `/process` | Generate collage & save metadata |
| GET | `/result/{id}` | Fetch session result |
| GET | `/sessions` | List all sessions |

---

### Quick start

#### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Install gphoto2 for Sony ZV-E10 support
# macOS:  brew install gphoto2
# Linux:  sudo apt install gphoto2

# Start the API server
cd photobooth-app/backend
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd photobooth-app/frontend
npm install
npm run dev          # opens http://localhost:5173
```

#### Legacy desktop app (PySide6)

```bash
pip install -r requirements.txt
python app/main.py
```
