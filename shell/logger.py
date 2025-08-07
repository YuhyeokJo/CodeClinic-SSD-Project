import os
import time
from datetime import datetime


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_dir="logs", max_size_kb=10):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.log_dir = log_dir
        self.max_size = max_size_kb * 1024  # 10KB
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "latest.log")
        self._rotate_if_needed()
        self._compress_if_needed()

        self._initialized = True

    @classmethod
    def _reset(cls):
        cls._instance = None

    def _get_formatted_time(self):
        return datetime.now().strftime("%y.%m.%d %H:%M")

    def _rotate_if_needed(self):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) >= self.max_size:
            ts = datetime.now().strftime("%y%m%d_%H%M")
            new_path = os.path.join(self.log_dir, f"until_{ts}.log")
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(self.log_file, new_path)

    def _compress_if_needed(self):
        log_files = sorted([
            f for f in os.listdir(self.log_dir)
            if f.startswith("until_") and f.endswith(".log")
        ])

        if len(log_files) >= 2:
            oldest = log_files[0]
            src = os.path.join(self.log_dir, oldest)
            dst = src.replace(".log", ".zip")
            os.rename(src, dst)

    def print(self, func_name: str, message: str):
        ts = self._get_formatted_time()
        func_display = func_name.ljust(30)
        full_message = f"[{ts}] {func_display}: {message}"

        self._rotate_if_needed()
        self._compress_if_needed()

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")


if __name__ == "__main__":
    logger = Logger()

    for i in range(300):
        logger.print("Shell.release()", f"테스트 로그 메시지 {i}")
        time.sleep(0.01)
