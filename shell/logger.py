import os
import time
from datetime import datetime


class Logger:
    def __init__(self, log_dir="logs", max_size_kb=10):
        self.log_dir = log_dir
        self.max_size = max_size_kb * 1024  # 10KB
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "latest.log")
        self._rotate_if_needed()
        self._compress_if_needed()

    def _get_formatted_time(self):
        return datetime.now().strftime("%y.%m.%d %H:%M")

    def _rotate_if_needed(self):
        pass

    def _compress_if_needed(self):
        pass

    def print(self, func_name: str, message: str):
        # 로그 메시지 구성
        ts = self._get_formatted_time()
        func_display = func_name.ljust(30)
        full_message = f"[{ts}] {func_display}: {message}"

        # 파일 회전 및 압축 조건 확인
        self._rotate_if_needed()
        self._compress_if_needed()

        # 로그 파일에 기록
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")


# 예제 사용
if __name__ == "__main__":
    logger = Logger()

    for i in range(300):
        logger.print("Shell.release()", f"테스트 로그 메시지 {i}")
        time.sleep(0.01)  # 너무 빨리 돌지 않도록 sleep
