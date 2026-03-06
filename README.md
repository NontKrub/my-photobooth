## PhotoBooth App

Features
- Sony camera workflow
- 4 or 6 photos per session
- Frame layout 4x6
- Canon Selphy printing
- QR code generation
- Session history

---

## Testing on macOS

### Prerequisites

- **Python 3.11** – the build is tested with 3.11; install with [Homebrew](https://brew.sh):
  ```bash
  brew install python@3.11
  ```
- **pip** (bundled with Python)

### 1 – Install dependencies

```bash
pip3.11 install -r requirements.txt
```

> **Note:** On Apple Silicon (M1/M2/M3) you may need to build the native extensions yourself:
> ```bash
> pip3.11 uninstall -y pillow watchdog
> ARCHFLAGS="-arch arm64" pip3.11 install --no-binary=:all: pillow watchdog
> ```

### 2 – Run the desktop app

```bash
cd photobooth-app   # repo root
MOCK_PRINTER=1 python3.11 app/main.py
```

Setting `MOCK_PRINTER=1` skips the `lpr` call so the app works without a Canon Selphy printer attached.

### 3 – Simulate camera input (no Sony camera required)

When the app starts a session it watches the folder:

```
~/Pictures/photobooth/input/
```

Copy any JPEG files there to trigger the photo-capture flow:

```bash
# In a second terminal – copy your test images one by one
cp /path/to/test1.jpg ~/Pictures/photobooth/input/
cp /path/to/test2.jpg ~/Pictures/photobooth/input/
# … repeat until the session photo target (4 or 6) is reached
```

The session window updates its counter after each file and automatically processes the session once the target is met.

### 4 – Run the web server (optional)

The web server serves captured sessions over HTTP so you can preview QR code links in a browser:

```bash
uvicorn web.server:app --reload --port 8000
```

Then open [http://localhost:8000/s/<session_id>](http://localhost:8000/s/) in a browser, where `<session_id>` is a timestamp directory name under `~/Pictures/photobooth/sessions/`.

### 5 – Build a standalone macOS app (optional)

```bash
pip3.11 install pyinstaller
pip3.11 uninstall -y pillow watchdog
ARCHFLAGS="-arch x86_64 -arch arm64" pip3.11 install --no-binary=:all: pillow watchdog
pyinstaller --windowed --target-arch universal2 --name PhotoBooth app/main.py
# Output: dist/PhotoBooth.app
open dist/PhotoBooth.app
```

---

## Quick-start (summary)

```bash
pip3.11 install -r requirements.txt
MOCK_PRINTER=1 python3.11 app/main.py
```
