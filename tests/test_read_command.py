from shell.commands.read import Read
from shell.driver import SSDDriver

INVALID_COMMAND = "INVALID COMMAND"

def test_execute_with_no_args(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = Read(ssd_driver)
    assert INVALID_COMMAND == readCommand.execute([])


def test_execute_with_too_many_args(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = Read(ssd_driver)
    assert INVALID_COMMAND == readCommand.execute(['123', '456'])


def test_execute_with_not_digit(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = Read(ssd_driver)
    assert INVALID_COMMAND == readCommand.execute(['12e'])


def test_execute_with_valid_arg(mocker, capsys):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = Read(ssd_driver)
    ssd_driver.read.return_value = "0x12345678"
    assert "[Read] LBA 42: 0x12345678" == readCommand.execute(['42'])
