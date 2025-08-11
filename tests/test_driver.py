from pathlib import Path

import pytest

from shell.driver import SSDDriver


def test_driver_read_mock(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)
    ssd_driver.read.return_value = "[Read] LBA 10: 0x12345678"
    result = ssd_driver.read("10")

    assert result == "[Read] LBA 10: 0x12345678"


def test_driver_write_mock(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)
    ssd_driver.write.return_value = f"[Write] Done"
    result = ssd_driver.write("10", "0x12345678")

    assert result == f"[Write] Done"


def test_driver_read():
    output_dir = Path(__file__).resolve().parent.parent / "output"
    ssd_nand_file = output_dir / "ssd_nand.txt"
    ssd_driver = SSDDriver()
    ssd_driver.flush()
    with open(ssd_nand_file, "w") as f:
        f.write("1 0x12345678")

    result = ssd_driver.read("1")

    assert result == "0x12345678"


def test_driver_read_write():
    ssd_driver = SSDDriver()
    assert ssd_driver.write("10", "0xAABBCCDD")

    result = ssd_driver.read("10")

    assert result == "0xAABBCCDD"
