import psutil


class SystemMetricsMonitor:
    def get_system_metrics(self):
        cpu = psutil.cpu_percent(interval=0)
        ram = psutil.virtual_memory()
        rom = psutil.disk_usage('/')
        return {
            "cpu": cpu,
            "ram_used": round(ram.used / (1024 ** 3), 2),  # В ГБ
            "ram_total": round(ram.total / (1024 ** 3), 2),  # В ГБ
            "rom_used": round(rom.used / (1024 ** 3), 2),  # В ГБ
            "rom_total": round(rom.total / (1024 ** 3), 2),  # В ГБ
        }
