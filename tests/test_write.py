import pytest
from pytest_mock import MockerFixture

from shell.commands.write import WriteCommand
from shell.driver import SSDDriver


def test_write_correctly(capsys, mocker: MockerFixture):
    """
    올바르게 인수가 전달되었고 ssd가 동작하므로 [WRITE] Done을 반환해야 함
    """
    #arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = WriteCommand(mocked_ssd)

    #act
    actual = write_command.execute(["3", "0x00000001"])

    #assert
    assert actual == "[WRITE] Done"


def test_write_wrongly_with_minus_lba(mocker: MockerFixture):
    """
    음수 lba가 전달되면 INVALID COMMAND를 반환해야 함
    """
    #arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = WriteCommand(mocked_ssd)

    #act
    actual = write_command.execute(["-1", "0x00000001"])

    #assert
    assert actual == "INVALID COMMAND"