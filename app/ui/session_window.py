from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from services.camera_watcher import CameraWatcher


class SessionWindow(QWidget):

    def __init__(self, session_manager):

        super().__init__()

        self.manager = session_manager

        self.layout = QVBoxLayout()

        self.label = QLabel("Waiting for photos")

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.watcher = CameraWatcher(self.manager, self.on_photo)

        self.watcher.start()

    def on_photo(self, count):

        self.label.setText(f"Photos captured {count}/{self.manager.photo_target}")

        if self.manager.is_complete():

            self.label.setText("Processing...")
            self.manager.process_session()