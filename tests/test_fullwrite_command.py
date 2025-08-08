from pytest_mock import MockerFixture

from shell.command_constants import INVALID_COMMAND
from shell.commands.fullwrite import FullWrite
from shell.driver import SSDDriver

DONE = "[FullWrite] Done"


def test_full_write_command_success(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = True
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xABCDFFFF']) == DONE
    assert driver.write.call_count == 100

    called_lbas = [call.args[0] for call in driver.write.call_args_list]
    assert called_lbas == [str(x) for x in range(100)]


def test_full_write_command_fail_empty_data(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = False
    full_write_command = FullWrite(driver)

    assert full_write_command.execute([]) == INVALID_COMMAND


def test_full_write_command_fail_wrong_data(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = False
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xAABCDFFFFFFF']) == INVALID_COMMAND
    assert full_write_command.execute(['0xAABCDFFFKF']) == INVALID_COMMAND
    assert full_write_command.execute(['0AABCDFFFKF']) == INVALID_COMMAND


def test_full_write_command_success_normalize_hex(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = True
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xAA']) == DONE
    assert full_write_command.execute(['0xF']) == DONE
    assert full_write_command.execute(['0x001']) == DONE


def test_full_write_command(mocker: MockerFixture):
    driver = SSDDriver()
    full_write_command = FullWrite(driver)

    assert full_write_command.execute(['0xABCDFFFF']) == DONE
