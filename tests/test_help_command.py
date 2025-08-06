import pytest
from pytest_mock import MockerFixture

from shell.commands.help import Help
from shell.driver import SSDDriver


def test_help_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    help_command.execute([]) == "[Help]"
