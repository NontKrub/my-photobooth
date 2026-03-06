from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import INPUT_DIR


class Handler(FileSystemEventHandler):

    def __init__(self, manager, callback):

        self.manager = manager
        self.callback = callback

    def on_created(self, event):

        if event.is_directory:
            return

        if event.src_path.lower().endswith(".jpg"):

            self.manager.add_photo(event.src_path)

            self.callback(len(self.manager.photos))


class CameraWatcher:

    def __init__(self, manager, callback):

        self.manager = manager
        self.callback = callback

        self.observer = Observer()

    def start(self):

        handler = Handler(self.manager, self.callback)

        self.observer.schedule(handler, str(INPUT_DIR), recursive=False)

        self.observer.start()