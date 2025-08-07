import random

from pytest_mock import MockerFixture
from shell.driver import SSDDriver
from scripts.script_runner import ScriptRunner

INVALID_COMMAND = "INVALID COMMAND"
SCRIPT_PASS = "PASS"
SCRIPT_FAIL = "FAIL"
SCRIPT_1_GROUP_SIZE = 5
SCRIPT_1_CALL_COUNT = 100
SCRIPT_2_LBA_SIZE = 5
SCRIPT_2_LOOP_SIZE = 30
SCRIPT_3_LBA_SIZE = 2
SCRIPT_3_LOOP_SIZE = 200
SCRIPT_4_LOOP_SIZE = 30
SCRIPT_4_GROUP_SIZE = 3
SCRIPT_4_GROUP_LENGTH = 48


def test_full_write_and_read_compare_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    inputs = script_runner._make_input_full_write_and_read_compare(SCRIPT_1_GROUP_SIZE)
    driver.read.side_effect = list(inputs.values())
    script_runner.full_write_and_read_compare()
    assert driver.write.call_count == SCRIPT_1_CALL_COUNT
    assert driver.read.call_count == SCRIPT_1_CALL_COUNT


def test_full_write_and_read_compare_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    inputs = script_runner._make_input_full_write_and_read_compare(SCRIPT_1_GROUP_SIZE)
    driver.read.side_effect = list(inputs.values())
    assert script_runner.full_write_and_read_compare() == SCRIPT_PASS


def test_full_write_and_read_compare_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    inputs = script_runner._make_input_full_write_and_read_compare(SCRIPT_1_GROUP_SIZE)
    input_values = list(inputs.values())
    input_values[3] = "0x00000000"
    driver.read.side_effect = input_values
    assert script_runner.full_write_and_read_compare() == SCRIPT_FAIL


def test_partial_lba_write_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    driver.read.side_effect = ["0x11112345"] * SCRIPT_2_LBA_SIZE * SCRIPT_2_LOOP_SIZE
    script_runner.partial_lba_write()
    assert driver.write.call_count == SCRIPT_2_LBA_SIZE * SCRIPT_2_LOOP_SIZE
    assert driver.read.call_count == SCRIPT_2_LBA_SIZE * SCRIPT_2_LOOP_SIZE


def test_partial_lba_write_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    driver.read.side_effect = ["0x11112345"] * SCRIPT_2_LBA_SIZE * SCRIPT_2_LOOP_SIZE
    assert script_runner.partial_lba_write() == SCRIPT_PASS


def test_partial_lba_write_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = ["0x11112345"] * SCRIPT_2_LBA_SIZE * SCRIPT_2_LOOP_SIZE
    input_values[3] = "0x00000000"
    driver.read.side_effect = input_values
    assert script_runner.partial_lba_write() == SCRIPT_FAIL


def test_write_read_aging_count(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = []
    for num_seed in script_runner.seeds:
        random.seed(num_seed)
        input_values.append(f"0x{random.randint(0, 0xFFFFFFFF):08X}")
    driver.read.side_effect = [value for value in input_values for _ in range(SCRIPT_3_LBA_SIZE)]
    script_runner.write_read_aging()
    assert driver.write.call_count == SCRIPT_3_LBA_SIZE * SCRIPT_3_LOOP_SIZE
    assert driver.read.call_count == SCRIPT_3_LBA_SIZE * SCRIPT_3_LOOP_SIZE


def test_write_read_aging_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = []
    for num_seed in script_runner.seeds:
        random.seed(num_seed)
        input_values.append(f"0x{random.randint(0, 0xFFFFFFFF):08X}")
    driver.read.side_effect = [value for value in input_values for _ in range(SCRIPT_3_LBA_SIZE)]
    assert script_runner.write_read_aging() == SCRIPT_PASS


def test_write_read_aging_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = []
    for num_seed in script_runner.seeds:
        random.seed(num_seed)
        input_values.append(f"0x{random.randint(0, 0xFFFFFFFF):08X}")
    driver.read.side_effect = input_values * SCRIPT_3_LBA_SIZE
    assert script_runner.write_read_aging() == SCRIPT_FAIL


def test_erase_and_write_aging_pass(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = ["0x00000000"] * SCRIPT_4_LOOP_SIZE * SCRIPT_4_GROUP_LENGTH * SCRIPT_4_GROUP_SIZE
    driver.read.side_effect = input_values
    assert script_runner.erase_and_write_aging() == SCRIPT_PASS


def test_erase_and_write_aging_fail(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    script_runner = ScriptRunner(driver)
    input_values = ["0x00000001"] * SCRIPT_4_LOOP_SIZE * SCRIPT_4_GROUP_LENGTH * SCRIPT_4_GROUP_SIZE
    driver.read.side_effect = input_values
    assert script_runner.erase_and_write_aging() == SCRIPT_FAIL
