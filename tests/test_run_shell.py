import pytest
from pytest_mock import MockerFixture

from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.commands.help import Help
from shell.commands.exit import Exit
from shell.driver import SSDDriver
from shell.run_shell import TestShell
from shell.run_shell import run_interactive_shell


def test_interactive_shell_correct_input(capsys, mocker):
    input_patch = mocker.patch("shell.run_shell.input")
    input_patch.side_effect = [
        "help write",
        "write 3 0x00000001",
        "read 3",
        "fullwrite 0x00000001",
        "fullread",
        "exit"
    ]

    run_interactive_shell()

    for output in capsys.readouterr().out.split("\n"):
        if output == "INVALID COMMAND":
            assert False


@pytest.mark.parametrize(
    "script_id", ["1_", "2_", "3_"]
)
def test_interactive_shell_using_script(capsys, mocker, script_id):
    input_patch = mocker.patch("shell.run_shell.input")
    input_patch.side_effect = [
        script_id,
        "exit"
    ]

    run_interactive_shell()

    assert capsys.readouterr().out.strip("\n").split("\n") == [
        "[SCRIPT] PASS",
        "[Exit]"
    ]


"""
Tests using moced ssd driver
"""


@pytest.fixture
def mocked_driver_shell_input(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    test_shell = TestShell(driver)
    input_patch = mocker.patch("shell.run_shell.input")

    return driver, test_shell, input_patch


def test_if_builtin_commands_are_registered(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    test_shell = TestShell(driver)

    assert isinstance(test_shell._commands["write"], Write)
    assert isinstance(test_shell._commands["read"], Read)
    assert isinstance(test_shell._commands["fullwrite"], FullWrite)
    assert isinstance(test_shell._commands["fullread"], FullRead)
    assert isinstance(test_shell._commands["exit"], Exit)
    assert isinstance(test_shell._commands["help"], Help)


def test_not_exist_command_and_exit(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    input_patch.side_effect = ["not_exist", "exit"]

    # Act
    test_shell.run()

    # Assert
    assert capsys.readouterr().out.strip("\n").split("\n") == [
        "INVALID COMMAND", "[Exit]"
    ]


def test_read_command_input_with_correct_command(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "[Read] LBA 3: 0x00000001"


def test_read_command_input_with_wrong_lba(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read -1", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "INVALID COMMAND"


def test_read_command_correctly_until_exit(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.side_effect = ["0x00000003"]
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "[Read] LBA 3: 0x00000003"
