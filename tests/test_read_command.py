from shell.commands.read import Read
from shell.driver import SSDDriver
from pathlib import Path

INVALID_COMMAND = "INVALID COMMAND"


def test_execute_with_no_args(mocker):
    ssd_driver = mocker.Mock(spec=SSDDriver)

    read_command = Read(ssd_driver)
    assert INVALID_COMMAND == read_command.execute([])


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

def test_read_command():
    output_dir = Path(__file__).resolve().parent.parent / "output"
    ssd_nand_file = output_dir / "ssd_nand.txt"
    with open(ssd_nand_file, "w") as f:
        f.write("42 0x12345678")


    ssd_driver = SSDDriver()
    readCommand = Read(ssd_driver)
    assert "[Read] LBA 42: 0x12345678" == readCommand.execute(['42'])