import pytest
from pytest_mock import MockerFixture

from shell.command_constants import INVALID_COMMAND
from shell.commands.erase import Erase
from shell.driver import SSDDriver

DONE = "[Erase] Done"


def test_erase_correctly(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = Erase(mocked_ssd)
    actual = erase_command.execute(["3", "1"])
    assert actual == DONE


def test_erase_correctly_with_over_size(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = Erase(mocked_ssd)
    actual = erase_command.execute(["99", "2"])
    assert actual == DONE


def test_erase_correctly_with_large_size(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = Erase(mocked_ssd)
    actual = erase_command.execute(["10", "30"])
    assert actual == DONE


@pytest.mark.parametrize(
    "wrong_argument", [
        ["100", "1"],
        ["-1", "5"],
    ]
)
def test_erase_invalid_result_with_wrong_argument(mocker: MockerFixture, wrong_argument):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    erase_command = Erase(mocked_ssd)
    actual = erase_command.execute(wrong_argument)
    assert actual == INVALID_COMMAND


def test_erase_correctly_with_ssd():
    driver = SSDDriver()
    erase_command = Erase(driver)
    actual = erase_command.execute(["3", "1"])
    assert actual == DONE


def test_erase_correctly_with_ssd_neg_size():
    driver = SSDDriver()
    erase_command = Erase(driver)
    actual = erase_command.execute(["3", "-2"])
    assert actual == DONE


def test_erase_correctly_with_ssd_zero_size():
    driver = SSDDriver()
    erase_command = Erase(driver)
    actual = erase_command.execute(["3", "0"])
    assert actual == DONE
