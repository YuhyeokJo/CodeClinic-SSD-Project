import pytest
from pytest_mock import MockerFixture

from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.driver import SSDDriver
from shell.test_shell import TestShell


def test_if_builtin_commands_are_registered(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    test_shell = TestShell(driver)

    assert isinstance(test_shell._commands["write"], Write)
    assert isinstance(test_shell._commands["read"], Read)
    assert isinstance(test_shell._commands["fullwrite"], FullWrite)
    assert isinstance(test_shell._commands["fullread"], FullRead)

def test_read_command_input(capsys, mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    test_shell = TestShell(driver)

    input_patch = mocker.patch("shell.test_shell.input")
    driver.read.return_value = "0x00000001"
    input_patch.return_value = "read 3"

    expected = "[Read] LBA 3: 0x00000001"
    test_shell.run()
    actual = capsys.readouterr().out.strip("\n")
    assert actual == expected


def test_read_command_input_with_wrong_lba(capsys, mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    test_shell = TestShell(driver)

    input_patch = mocker.patch("shell.test_shell.input")
    driver.read.return_value = "0x00000001"
    input_patch.return_value = "read -1"

    expected = "LBA must be a number\n[Read] INVALID COMMAND"
    test_shell.run()
    actual = capsys.readouterr().out.strip("\n")
    assert actual == expected
