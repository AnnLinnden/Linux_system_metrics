from PyQt5.QtWidgets import QApplication
from .app_window import SystemMonitorWindow


def main():
    app = QApplication([])
    app_window = SystemMonitorWindow()
    app_window.show()
    app.exec()


if __name__ == "__main__":
    main()
