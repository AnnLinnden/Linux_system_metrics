import sqlite3
import datetime


class DatabaseHandler:
    def __init__(self, db_path="system_monitoring_data.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            время TEXT,
            ЦП REAL,
            ОЗУ REAL,
            ПЗУ REAL
        )
        """)
        self.connection.commit()

    def insert_data(self, cpu, ram, rom):
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute("""
        INSERT INTO system_metrics (время, ЦП, ОЗУ, ПЗУ)
        VALUES (?, ?, ?, ?)
        """, (timestamp, cpu, ram, rom))
        self.connection.commit()

    def close(self):
        self.connection.close()
