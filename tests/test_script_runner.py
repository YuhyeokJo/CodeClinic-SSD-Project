from pytest_mock import MockerFixture
from shell.driver import SSDDriver
from scripts.script_runner import ScriptRunner

INVALID_COMMAND = "[SCRIPT] INVALID COMMAND"


def test_full_write_and_read_compare_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    script_runner.full_write_and_read_compare()
    assert driver.write.call_count == 100
    assert driver.read.call_count == 100


def test_full_write_and_read_compare_result(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    group_size = 5
    inputs = script_runner._make_input_full_write_and_read_compare(group_size)
    driver.read.side_effect = list(inputs.values())
    assert script_runner.full_write_and_read_compare() == "[SCRIPT] PASS"
