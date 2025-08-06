from pytest_mock import mocker
from shell.driver import SSDDriver


def test_driver_read(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)
    ssd_driver.read.return_value = "[Read] LBA 10: 0x12345678"
    result = ssd_driver.read("10")

    assert result == "[Read] LBA 10: 0x12345678"

def test_driver_write(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)
    ssd_driver.write.return_value = f"[Write] Done"
    result = ssd_driver.write("10", "0x12345678")

    assert result == f"[Write] Done"
