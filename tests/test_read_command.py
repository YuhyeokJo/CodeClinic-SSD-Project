from shell.commands.read import ReadCommand
from shell.driver import SSDDriver

INVALID_COMMAND = "[READ] INVALID COMMAND"

def test_execute_with_no_args(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = ReadCommand(ssd_driver)
    assert INVALID_COMMAND == readCommand.execute([])


def test_execute_with_too_many_args(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = ReadCommand(ssd_driver)
    assert INVALID_COMMAND == readCommand.execute(['123', '456'])


def test_execute_with_valid_arg(mocker, capsys):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = ReadCommand(ssd_driver)
    ssd_driver.read.return_value = "0x12345678"
    assert "[READ] LBA 42: 0x12345678" == readCommand.execute(['42'])
