from pytest_mock import MockerFixture
from shell.driver import SSDDriver
from shell.commands.fullread import Fullread


def test_fullread_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    full_reader = Fullread(driver)
    full_reader.run()
    assert driver.read.call_count == 100


def test_fullread_result(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    expected_output = [f"0x{lba:08X}" for lba in range(100)]
    driver.read.side_effect = expected_output
    full_reader = Fullread(driver)
    assert full_reader.run() == {lba: value for lba, value in enumerate(expected_output)}
