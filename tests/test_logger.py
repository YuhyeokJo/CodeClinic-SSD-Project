import os
import unittest
import tempfile
import time

from shell.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        # 테스트용 임시 디렉토리 생성
        self.test_dir = tempfile.TemporaryDirectory()
        self.logger = Logger(log_dir=self.test_dir.name, max_size_kb=0.01)  # 1KB로 회전 빨리 확인

    def tearDown(self):
        self.test_dir.cleanup()

    def test_log_file_created(self):
        self.logger.print("TestLogger.test_log_file_created()", "로그 메시지")
        log_path = os.path.join(self.test_dir.name, "latest.log")
        self.assertTrue(os.path.exists(log_path))

    def test_log_format(self):
        self.logger.print("TestLogger.test_log_format()", "포맷 테스트")
        log_path = os.path.join(self.test_dir.name, "latest.log")
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("TestLogger.test_log_format()", content)
            self.assertIn("포맷 테스트", content)
            self.assertRegex(content, r"\[\d{2}\.\d{2}\.\d{2} \d{2}:\d{2}\]")


if __name__ == "__main__":
    unittest.main()
