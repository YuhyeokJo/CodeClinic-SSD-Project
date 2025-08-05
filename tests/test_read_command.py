from shell.commands.read import ReadCommand
from shell.driver import SSDDriver


def test_execute_with_valid_arg(mocker, capsys):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    readCommand = ReadCommand(ssd_driver)
    ssd_driver.read.return_value = "0x12345678"
    assert "[READ] LBA 42: 0x12345678" == readCommand.execute(['42'])
