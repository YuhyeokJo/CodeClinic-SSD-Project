import random

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


def test_full_write_and_read_compare_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    group_size = 5
    inputs = script_runner._make_input_full_write_and_read_compare(group_size)
    driver.read.side_effect = list(inputs.values())
    assert script_runner.full_write_and_read_compare() == "[SCRIPT] PASS"


def test_full_write_and_read_compare_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    group_size = 5
    inputs = script_runner._make_input_full_write_and_read_compare(group_size)
    input_values = list(inputs.values())
    input_values[3] = "0x00000000"
    driver.read.side_effect = input_values
    assert script_runner.full_write_and_read_compare() == "[SCRIPT] FAIL"


def test_partial_lba_write_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    script_runner.partial_lba_write()
    assert driver.write.call_count == 150
    assert driver.read.call_count == 150


def test_partial_lba_write_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    driver.read.side_effect = ["0x11112345"] * 150
    assert script_runner.partial_lba_write() == "[SCRIPT] PASS"


def test_partial_lba_write_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = ["0x11112345"] * 150
    input_values[3] = "0x00000000"
    driver.read.side_effect = input_values
    assert script_runner.partial_lba_write() == "[SCRIPT] FAIL"


def test_write_read_aging_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    script_runner.write_read_aging()
    assert driver.write.call_count == 400
    assert driver.read.call_count == 400


def test_write_read_aging_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    random.seed(42)
    value = f"0x{random.randint(0, 0xFFFFFFFF):08X}"
    driver.read.side_effect = [value] * 400
    assert script_runner.write_read_aging() == "[SCRIPT] PASS"


def test_write_read_aging_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    random.seed(42)
    value = f"0x{random.randint(0, 0xFFFFFFFF):08X}"
    input_values = [value] * 400
    input_values[3] = "0x00000000"
    driver.read.side_effect = input_values
    assert script_runner.write_read_aging() == "[SCRIPT] FAIL"
