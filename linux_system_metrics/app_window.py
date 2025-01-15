from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDoubleSpinBox
from PyQt5.QtCore import QTimer, QTime, Qt

import matplotlib
matplotlib.use('Qt5Agg')  # эту строку вниз не опускать, иначе не сработают импорты! Игнорим PEP8 здесь
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from linux_system_metrics.system_monitoring import SystemMetricsMonitor
from linux_system_metrics.database_handler import DatabaseHandler


class SystemMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мониторинг показателей")
        self.setFixedSize(800, 900)

        self.system_monitor = SystemMetricsMonitor()
        self.database = DatabaseHandler()
        self.database.create_table()
        self.is_recording = False

        layout = QVBoxLayout()
        widget = QWidget()

        self.choice_refresh_time_label = QLabel("Выберите частоту обновления показателей в секундах: ")
        self.choice_refresh_time_label.setStyleSheet("font-size: 16px;")
        self.choice_refresh_time = QDoubleSpinBox()
        self.choice_refresh_time.setStyleSheet("font-size: 16px;")
        self.choice_refresh_time.setRange(0.5, 10)
        self.choice_refresh_time.setValue(1)
        self.choice_refresh_time.setSingleStep(0.5)
        self.choice_refresh_time.valueChanged.connect(self.change_timer_interval)

        self.cpu_label = QLabel("ЦП: -")
        self.cpu_label.setStyleSheet("font-size: 16px;")
        self.ram_label = QLabel("ОЗУ: -")
        self.ram_label.setStyleSheet("font-size: 16px;")
        self.rom_label = QLabel("ПЗУ: -")
        self.rom_label.setStyleSheet("font-size: 16px;")

        self.cpu_canvas = self.create_chart_canvas("ЦП (%)")
        self.ram_canvas = self.create_chart_canvas("ОЗУ (ГБ)")
        self.rom_canvas = self.create_chart_canvas("ПЗУ (ГБ)")

        self.create_graph_layout(layout)

        self.start_rec_button = QPushButton("Начать запись")
        self.start_rec_button.setStyleSheet("font-size: 20px; padding: 5px")
        self.start_rec_button.clicked.connect(self.start_recording)

        self.finish_rec_button = QPushButton("Закончить запись")
        self.finish_rec_button.setStyleSheet("font-size: 20px; padding: 5px")
        self.finish_rec_button.clicked.connect(self.stop_recording)
        self.finish_rec_button.setVisible(False)

        self.record_timer_label = QLabel("Данные в БД не записываются")
        self.record_timer_label.setStyleSheet("font-size: 17px;")
        self.record_time = QTime(0, 0, 0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(int(self.choice_refresh_time.value() * 1000))

        self.record_timer = QTimer()
        self.record_timer.timeout.connect(self.update_record_time)

        widgets = [self.choice_refresh_time,
                   self.cpu_label,
                   self.ram_label,
                   self.rom_label,
                   self.start_rec_button,
                   self.finish_rec_button,
                   self.record_timer_label]

        for one_widget in widgets:
            layout.addWidget(one_widget, alignment=Qt.AlignHCenter)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_chart_canvas(self, title):
        figure = Figure(figsize=(6, 2))  # ширина и высота графика в дюймах
        canvas = FigureCanvasQTAgg(figure)
        yx_graph = figure.add_subplot(111)  # строка 1, столбец 1, график первый
        yx_graph.set_title(title, fontsize=10)
        yx_graph.set_xlim(0, 20)
        yx_graph.set_ylim(0, 100)
        yx_graph.margins(0)
        yx_graph.tick_params(axis='both', which='major', labelsize=8)
        yx_graph.grid()
        canvas.ax = yx_graph
        canvas.data = [0] * 20  # нули, которые отображаются на старте, пока график заполняется актуальными значениями
        return canvas

    def create_graph_layout(self, layout):
        graph_layouts = [
            (self.choice_refresh_time_label, self.choice_refresh_time),
            (self.cpu_label, self.cpu_canvas),
            (self.ram_label, self.ram_canvas),
            (self.rom_label, self.rom_canvas),
        ]

        for label, canvas in graph_layouts:
            h_layout = QHBoxLayout()
            h_layout.addWidget(label, alignment=Qt.AlignLeft)
            h_layout.addWidget(canvas, alignment=Qt.AlignLeft)
            layout.addLayout(h_layout)

    def update_chart(self, canvas, value):
        canvas.data.pop(0)
        canvas.data.append(value)
        canvas.ax.clear()
        canvas.ax.plot(canvas.data, '-o', markersize=3)
        canvas.ax.set_xlim(0, 20)
        canvas.ax.set_ylim(0, 100)
        canvas.ax.grid()
        canvas.draw()

    def start_recording(self):
        self.start_rec_button.setVisible(False)
        self.finish_rec_button.setVisible(True)
        self.is_recording = True
        self.record_time = QTime(0, 0, 0)
        self.record_timer.start(1000)

        #  эта строка нужна, чтобы текст изменился сразу после нажатия на кнопку, а не через секунду,
        #  т.е. пользователь получает мгновенную обратную связь.
        #  Дальше текст будет обновлять update_record_time
        self.record_timer_label.setText("Начинаю запись в БД")

    def stop_recording(self):
        self.finish_rec_button.setVisible(False)
        self.start_rec_button.setVisible(True)
        self.is_recording = False
        self.record_timer.stop()
        self.record_timer_label.setText("Запись в БД остановлена")

    def update_record_time(self):
        self.record_time = self.record_time.addSecs(1)
        self.record_timer_label.setText(f"Запись в БД идет: {self.record_time.toString('hh:mm:ss')}")

    def recording_to_db(self, cpu, ram, rom):
        self.database.insert_data(cpu, ram, rom)

    def change_timer_interval(self):
        self.timer.setInterval(int(self.choice_refresh_time.value() * 1000))  # *1000 - переводим из мс в с

    def update_metrics(self):
        metrics = self.system_monitor.get_system_metrics()
        self.cpu_label.setText(f"ЦП: {metrics['cpu']}%")
        self.ram_label.setText(f"ОЗУ: {metrics['ram_used']}/{metrics['ram_total']} ГБ")
        self.rom_label.setText(f"ПЗУ: {metrics['rom_used']}/{metrics['rom_total']} ГБ")

        self.update_chart(self.cpu_canvas, metrics['cpu'])
        self.update_chart(self.ram_canvas, (metrics['ram_used'] / metrics['ram_total']) * 100)
        self.update_chart(self.rom_canvas, (metrics['rom_used'] / metrics['rom_total']) * 100)

        if self.is_recording:
            self.recording_to_db(metrics['cpu'], metrics['ram_used'], metrics['rom_used'])
