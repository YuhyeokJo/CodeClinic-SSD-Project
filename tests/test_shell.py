import pytest
from pytest_mock import MockerFixture

from shell.commands.fullread import Fullread
from shell.commands.fullwrite import FullWrite
from shell.commands.read import ReadCommand
from shell.commands.write import WriteCommand
from shell.driver import SSDDriver
from shell.test_shell import TestShell


def test_if_builtin_commands_are_registered(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    test_shell = TestShell(driver)

    assert isinstance(test_shell._commands["write"], WriteCommand)
    assert isinstance(test_shell._commands["read"], ReadCommand)
    assert isinstance(test_shell._commands["fullwrite"], FullWrite)
    assert isinstance(test_shell._commands["fullread"], Fullread)
