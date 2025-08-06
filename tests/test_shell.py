import pytest
from pytest_mock import MockerFixture

from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.driver import SSDDriver
from shell.test_shell import TestShell

@pytest.fixture
def mocked_driver_shell_input(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    test_shell = TestShell(driver)
    input_patch = mocker.patch("shell.test_shell.input")

    return driver, test_shell, input_patch

def test_if_builtin_commands_are_registered(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    test_shell = TestShell(driver)

    assert isinstance(test_shell._commands["write"], Write)
    assert isinstance(test_shell._commands["read"], Read)
    assert isinstance(test_shell._commands["fullwrite"], FullWrite)
    assert isinstance(test_shell._commands["fullread"], FullRead)

def test_read_command_input_with_correct_command(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n")
    assert last_shell_line == "[Read] LBA 3: 0x00000001"


def test_read_command_input_with_wrong_lba(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read -1", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-1]
    assert last_shell_line == "[Read] INVALID COMMAND"


def test_read_command_correctly_until_exit(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.side_effect = ["0x00000003"]
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-1]
    assert last_shell_line == "[Read] LBA 3: 0x00000003"