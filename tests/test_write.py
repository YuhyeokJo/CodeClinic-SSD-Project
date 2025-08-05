import pytest
from pytest_mock import MockerFixture

from shell.commands.write import WriteCommand
from shell.driver import SSDDriver


def test_write_correctly(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = WriteCommand(mocked_ssd)

    actual = write_command.execute(["3", "0x00000001"])

    assert actual == "[WRITE] Done"


def test_write_wrongly_with_minus_lba(mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = False
    write_command = WriteCommand(mocked_ssd)

    actual = write_command.execute(["-1", "0x00000001"])

    assert actual == "INVALID COMMAND"