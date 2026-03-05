from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)

from services.session_manager import SessionManager
from ui.session_window import SessionWindow


class HomeWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PhotoBooth")

        self.layout = QVBoxLayout()

        self.title = QLabel("PHOTO BOOTH")

        self.frame_select = QComboBox()
        self.frame_select.addItems(["default"])

        self.photo_count = QComboBox()
        self.photo_count.addItems(["4", "6"])

        self.start_button = QPushButton("START SESSION")

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.frame_select)
        self.layout.addWidget(self.photo_count)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start_session)

    def start_session(self):

        count = int(self.photo_count.currentText())

        manager = SessionManager(count)

        self.session_window = SessionWindow(manager)

        self.session_window.show()

        self.close()