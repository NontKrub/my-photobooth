from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from database.db import get_sessions


class HistoryWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()

        sessions = get_sessions()

        for s in sessions:

            label = QLabel(str(s))

            self.layout.addWidget(label)

        self.setLayout(self.layout)