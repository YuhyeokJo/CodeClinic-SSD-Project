from pytest_mock import MockerFixture

from shell.commands.fullwrite import FullWrite
from shell.driver import SSDDriver


def test_full_write_command(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    driver.write.return_value = True
    full_write_command = FullWrite(driver)
    assert full_write_command.execute(['0xABCDFFFF'])
