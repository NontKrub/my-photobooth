import sys
from PySide6.QtWidgets import QApplication
from ui.home_window import HomeWindow
from config import init_directories


def main():
    init_directories()

    app = QApplication(sys.argv)

    window = HomeWindow()
    window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()