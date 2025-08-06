from pytest_mock import MockerFixture
from shell.driver import SSDDriver
from shell.commands.exit import Exit


def test_exit(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    exit_command = Exit(driver)
    assert exit_command.execute([]) == "[Exit]"