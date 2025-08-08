import pytest
from pytest_mock import MockerFixture

from shell.commands.fullwrite import FullWrite
from shell.driver import SSDDriver
from shell.commands.fullread import FullRead


def test_fullread_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    expected_output = [f"0x{lba:08X}" for lba in range(100)]
    driver.read.side_effect = expected_output
    full_reader = FullRead(driver)
    full_reader.execute([])
    assert driver.read.call_count == 100


def test_fullread_result(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    expected_output = [f"0x{lba:08X}" for lba in range(100)]
    driver.read.side_effect = expected_output
    full_reader = FullRead(driver)
    result = ""
    for lba, value in enumerate(expected_output):
        result += f"\n [Read] LBA {lba}: {value}"
    assert full_reader.execute([]) == result


@pytest.mark.skip(reason="command buffer의 fastread가 아직 준비 되지 않았습니다.")
def test_fullread_command(mocker: MockerFixture):
    driver = SSDDriver()
    full_write = FullWrite(driver)
    full_write.execute(["0xABCDFFFF"])
    full_reader = FullRead(driver)
    result = ""
    for lba in range(100):
        result += f"\n [Read] LBA {lba}: 0xABCDFFFF"
    assert full_reader.execute([]) == result
