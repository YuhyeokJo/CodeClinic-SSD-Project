import os
import tempfile
import time
import pytest

from shell.logger import Logger


@pytest.fixture
def logger_with_tempdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        Logger._reset()
        logger = Logger(log_dir=tmpdir, max_size_kb=0.01)
        yield logger, tmpdir
        Logger._reset()


def test_log_file_created(logger_with_tempdir):
    logger, log_dir = logger_with_tempdir
    logger.print("TestLogger.test_log_file_created()", "로그 메시지")

    log_path = os.path.join(log_dir, "latest.log")
    assert os.path.exists(log_path)


def test_log_format(logger_with_tempdir):
    logger, log_dir = logger_with_tempdir
    logger.print("TestLogger.test_log_format()", "포맷 테스트")

    log_path = os.path.join(log_dir, "latest.log")
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "TestLogger.test_log_format()" in content
        assert "포맷 테스트" in content
        assert __import__("re").search(r"\[\d{2}\.\d{2}\.\d{2} \d{2}:\d{2}\:\d{2}\]", content)


def test_log_rotation(logger_with_tempdir):
    logger, log_dir = logger_with_tempdir

    for _ in range(200):
        logger.print("TestLogger.test_log_rotation()", "많이 쓰기")

    files = os.listdir(log_dir)
    log_files = [f for f in files if f.endswith(".log")]
    assert len(log_files) >= 2


@pytest.mark.skip(reason="수행 시간이 길어 기본 테스트에서 제외됨")
def test_log_compression(logger_with_tempdir):
    logger, log_dir = logger_with_tempdir

    for _ in range(10000):
        logger.print("TestLogger.test_log_compression()", "압축 조건 만족")
        time.sleep(0.01)

    files = os.listdir(log_dir)
    zip_files = [f for f in files if f.endswith(".zip")]
    assert len(zip_files) >= 1


def test_singleton():
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2
