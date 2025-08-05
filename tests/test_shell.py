import pytest
from pytest_mock import MockerFixture

from shell.commands.fullwrite import FullWrite
from shell.driver import SSDDriver


def test_full_write_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = True
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xABCDFFFF'])
    assert driver.write.call_count == 100

    called_lbas = [call.args[0] for call in driver.write.call_args_list]
    assert called_lbas == [str(x) for x in range(100)]

def test_full_write_command_fail_empty_data(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = False
    full_write_command = FullWrite(driver)

    assert full_write_command.execute([]) is False

def test_full_write_command_fail_wrong_data(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = False
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xAABCDFFFFFFF']) is False
