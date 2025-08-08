import pytest
from pytest_mock import MockerFixture

from shell.command_constants import INVALID_COMMAND
from shell.commands.erase_range import EraseRange
from shell.driver import SSDDriver

DONE = "[EraseRange] Done"


def test_erase_range_correctly(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = EraseRange(mocked_ssd)
    actual = erase_command.execute(["3", "10"])
    assert actual == DONE


def test_erase_range_correctly_with_over_size(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = EraseRange(mocked_ssd)
    actual = erase_command.execute(["99", "102"])
    assert actual == DONE


def test_erase_range_correctly_with_reverse_argument(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = EraseRange(mocked_ssd)
    actual = erase_command.execute(["50", "40"])
    assert actual == DONE


@pytest.mark.parametrize(
    "wrong_argument", [
        ["10", "-12"],
        ["100", "101"],
        ["-1", "5"],
    ]
)
def test_erase_range_invalid_result_with_wrong_argument(mocker: MockerFixture, wrong_argument):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = EraseRange(mocked_ssd)
    actual = erase_command.execute(wrong_argument)
    assert actual == INVALID_COMMAND


def test_erase_range_correctly_with_ssd():
    driver = SSDDriver()
    erase_command = EraseRange(driver)
    actual = erase_command.execute(["3", "10"])
    assert actual == DONE
