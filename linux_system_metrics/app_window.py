from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QDoubleSpinBox
from PyQt5.QtCore import QTimer
class SystemMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мониторинг показателей")
        self.setFixedSize(700, 700)

        layout = QVBoxLayout()
        widget = QWidget()

        self.choice_refresh_time = QDoubleSpinBox()
        self.choice_refresh_time.setRange(0.5, 10)
        self.choice_refresh_time.setValue(1)
        self.choice_refresh_time.setSingleStep(0.5)
        self.choice_refresh_time.valueChanged.connect(self.change_timer_interval)

        self.cpu_label = QLabel("ЦП: ")
        self.ram_label = QLabel("ОЗУ: ")
        self.rom_label = QLabel("ПЗУ: ")

        self.start_rec = QPushButton("Начать запись")
        self.start_rec.clicked.connect(self.start_recording)

        self.finish_rec = QPushButton("Закончить запись")
        self.finish_rec.clicked.connect(self.stop_recording)
        self.finish_rec.setVisible(False)

        self.timer = QTimer()
        # self.timer.timeout.connect(self.update_system_metrics)
        self.timer.start(int(self.choice_refresh_time.value() * 1000))

        widgets = [self.choice_refresh_time,
                   self.cpu_label,
                   self.ram_label,
                   self.rom_label,
                   self.start_rec,
                   self.finish_rec]

        for one_widget in widgets:
            layout.addWidget(one_widget)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_recording(self):  # Добавить запись в БД и включение таймера
        self.start_rec.setVisible(False)
        self.finish_rec.setVisible(True)

    def stop_recording(self):  # Остановить запись в БД и выключить таймер
        self.finish_rec.setVisible(False)
        self.start_rec.setVisible(True)

    def change_timer_interval(self):
        self.timer.setInterval(int(self.choice_refresh_time.value() * 1000))
