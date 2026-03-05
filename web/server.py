from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE = Path.home() / "Pictures" / "photobooth" / "sessions"

app = FastAPI()

app.mount("/sessions", StaticFiles(directory=BASE), name="sessions")


@app.get("/s/{session_id}", response_class=HTMLResponse)
def show_session(session_id: str):

    session_dir = BASE / session_id

    photos = sorted(session_dir.glob("photo*.jpg"))

    html = "<h1>PhotoBooth</h1>"

    gif = session_dir / "preview.gif"

    if gif.exists():
        html += f'<img src="/sessions/{session_id}/preview.gif"><br>'

    for p in photos:

        html += f'<img width=200 src="/sessions/{session_id}/{p.name}">'

    html += f'<br><a href="/sessions/{session_id}/final.jpg">Download Final Photo</a>'

    return html