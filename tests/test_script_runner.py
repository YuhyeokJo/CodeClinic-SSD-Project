from pytest_mock import MockerFixture
from shell.driver import SSDDriver
from shell.commands.script import Script

INVALID_COMMAND = "[SCRIPT] INVALID COMMAND"


def test_execute_with_no_args(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script = Script(driver)
    assert INVALID_COMMAND == script.execute([])


def test_execute_with_too_many_args(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script = Script(driver)
    assert INVALID_COMMAND == script.execute(['123', '456'])


def test_execute_with_not_digit(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script = Script(driver)
    assert INVALID_COMMAND == script.execute(['12e'])


# def test_execute_write(mocker: MockerFixture):
#     driver = mocker.Mock(spec=SSDDriver)
#     script = Script(driver)
#     script.execute(["3", "0x00000001"])
#     assert driver.write.call_count == 1


def test_execute_with_valid_arg(mocker, capsys):
    driver = mocker.Mock(spec=SSDDriver)
    script = Script(driver)
    driver.read.return_value = "0x12345678"
    assert "[SCRIPT] PASS" == script.execute(["3", "0x12345678"])
