import pytest
from pytest_mock import MockerFixture

from shell.command_constants import INVALID_COMMAND
from shell.commands.write import Write
from shell.driver import SSDDriver

DONE = "[Write] Done"


def test_write_correctly(capsys, mocker: MockerFixture):
    """
    올바르게 인수가 전달되었고 ssd가 동작하므로 [WRITE] Done을 반환해야 함
    """
    # arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    # act
    actual = write_command.execute(["3", "0x00000001"])

    # assert
    assert actual == "[Write] Done"


def test_write_correctly_after_normalize_hex(capsys, mocker: MockerFixture):
    """
    올바르게 인수가 전달되었고 ssd가 동작하므로 [WRITE] Done을 반환해야 함
    """
    # arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    # assert
    assert write_command.execute(["3", "0x000001"]) == DONE
    assert write_command.execute(["3", "0x00000FD"]) == DONE


@pytest.mark.parametrize(
    "wrong_argument", [
        ["-1", "0x00000001"],
        ["-1", "0x00000001", "additional"],
    ]
)
def test_write_wrongly_with_minus_lba(mocker: MockerFixture, wrong_argument):
    """
    음수 lba가 전달되면 INVALID COMMAND를 반환해야 함
    """
    # arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    for wrong_arg in wrong_argument:
        # act
        actual = write_command.execute(wrong_arg)

        # assert
        assert actual == INVALID_COMMAND


def test_write_command():
    ssd_driver = SSDDriver()
    writeCommand = Write(ssd_driver)

    assert DONE == writeCommand.execute(['42', "0x12345678"])

def test_if_write_command_normalize_hex_data(mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    write_command.execute(["3", "0x010"])
    mocked_ssd.write.assert_called_with("3", "0x00000010")
