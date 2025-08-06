import pytest
from pytest_mock import MockerFixture

from shell.commands.help import Help
from shell.driver import SSDDriver


def test_help_read_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute(['read']) == """
                SSD Test Shell Tool
                Team: ✨Code Clinic✨
                Author: 조유혁(팀장님), 강동협, 김혜원, 배정은, 조보근
                Command: read
                Usage & Description: read <LBA> <Value> (Reads value from given LBA)
                """


def test_help_write_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute(['Write']) == """
                SSD Test Shell Tool
                Team: ✨Code Clinic✨
                Author: 조유혁(팀장님), 강동협, 김혜원, 배정은, 조보근
                Command: write
                Usage & Description: write <LBA> (Writes value to LBA)
                """


def test_help_fullread_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute(['fullread']) == """
                SSD Test Shell Tool
                Team: ✨Code Clinic✨
                Author: 조유혁(팀장님), 강동협, 김혜원, 배정은, 조보근
                Command: fullread
                Usage & Description: fullread: (Reads value from all LBA(0~99))
                """


def test_help_fullwrite_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute(['fullwrite']) == """
                SSD Test Shell Tool
                Team: ✨Code Clinic✨
                Author: 조유혁(팀장님), 강동협, 김혜원, 배정은, 조보근
                Command: fullwrite
                Usage & Description: fullwrite <Value> (Writes value to all LBA(0~99))
                """


def test_help_unknown_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute(['red']) == f"Unknown command: red"


def test_help_empty_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    help_command = Help(driver)
    assert help_command.execute([]) == """Available commands:\n- read\n- write\n- fullread\n- fullwrite\n- exit"""
