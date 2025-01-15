from PyQt5.QtWidgets import QApplication
from linux_system_metrics.app_window import SystemMonitorWindow


def main():
    app = QApplication([])
    app_window = SystemMonitorWindow()
    app_window.show()
    app.exec()


if __name__ == "__main__":
    main()
