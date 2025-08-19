import os
from datetime import datetime

# ------------
# CLASE LOGGER
class FileLogger:
    def __init__(self, log_dir=None, log_name=None):
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), '../../test/log')
        if log_name is None:
            log_name = 'app.log'
        self.log_dir = os.path.abspath(log_dir)
        names = ["INFO","WARNING","ERROR"]
        for name in names:
            setattr(self, f"log_file_{name}", os.path.join(self.log_dir, f"{log_name}_{name.lower()}.log"))
            os.makedirs(self.log_dir, exist_ok=True)

    def log(self, message, level='INFO'):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{now}] [{level}] {message}\n"
        with open(getattr(self, f"log_file_{level}"), 'a', encoding='utf-8') as f:
            f.write(log_line)

    def info(self, message):
        self.log(message, level='INFO')

    def warning(self, message):
        self.log(message, level='WARNING')

    def error(self, message):
        self.log(message, level='ERROR')
