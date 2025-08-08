import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))

import pytest
import shutil

from dataclasses import dataclass
from pytest_mock import MockerFixture

from device import ssd
from device.ssd import SSD, INITIALIZED_DATA, ERROR, OUTPUT_DIR, NAND, OutputWriter, Validator
from device.command_buffer import CommandBuffer



@dataclass
class WriteCommand:
    cmd: str
    lba: str
    value: str


@pytest.fixture
def ssd_instance():
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    command_buffer = CommandBuffer()

    ssd1 = SSD(nand=NAND(OUTPUT_DIR),
               validator=Validator(),
               output_writer=OutputWriter(OUTPUT_DIR / "ssd_output.txt"),
               command_buffer=command_buffer
               )

    command_buffer.on_flush_callback = ssd1.flush
    command_buffer.initialize_buffer()
    return ssd1


def test_main_write_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    sys.argv = ['ssd.py', 'W', '10', '0xAAAABBBB']
    ssd.main()

    mock_ssd.write.assert_called_once_with('10', '0xAAAABBBB')
    mock_ssd.read.assert_not_called()
    mock_ssd.erase.assert_not_called()


def test_main_read_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    sys.argv = ['ssd.py', 'R', '10']
    ssd.main()

    mock_ssd.read.assert_called_once_with('10')
    mock_ssd.write.assert_not_called()
    mock_ssd.erase.assert_not_called()


def test_main_erase_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    sys.argv = ['ssd.py', 'E', '10', '5']
    ssd.main()

    mock_ssd.erase.assert_called_once_with('10', '5')
    mock_ssd.read.assert_not_called()
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize("invalid_lba", [
    'K',
    'a'
])
def test_main_other_command(ssd_instance, mocker: MockerFixture, invalid_lba, capsys):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    sys.argv = ['ssd.py', invalid_lba, '10']
    with pytest.raises(SystemExit):
        ssd.main()

    capsys.readouterr()
    mock_ssd.read.assert_not_called()
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize("invalid_lba", [
    'error',
    "0xB"
])
def test_lba_should_be_decimal(ssd_instance, mocker: MockerFixture, invalid_lba, capsys):
    """
    [LBA] : 10진수로 입력 받음
    """
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)

    sys.argv = ['ssd.py', 'W', invalid_lba, "0xAAAABBBB"]
    with pytest.raises(SystemExit):
        ssd.main()

    capsys.readouterr()
    mock_ssd.read.assert_not_called()
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize("invalid_value", [
    "AA",
    "0xa",
    "0xAAAABBBBBB",
])
def test_value_always_startswith_0x_and_length_10(ssd_instance, mocker: MockerFixture, invalid_value, capsys):
    """
    [Value] : 항상 0x가 붙으며 10 글자로 표기한다. ( 0x00000000  ~  0xFFFFFFFF)
    """
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)

    sys.argv = ['ssd.py', 'W', '2', invalid_value]
    with pytest.raises(SystemExit):
        ssd.main()
    capsys.readouterr()
    mock_ssd.read.assert_not_called()
    mock_ssd.write.assert_not_called()


def test_write_when_no_ssd_nand_text_create_then_write(ssd_instance):
    """
    ssd_nand.txt 파일이 없는 경우, 생성 후 데이터가 기록되어야 한다.
    """
    # arrange
    cmd = WriteCommand(cmd="W", lba='2', value='0xAAAABBBB')

    # act
    ssd_instance.write(cmd.lba, cmd.value)
    ssd_instance.flush()

    with open(ssd_instance.nand.path, "r") as f:
        lines = f.read()

    # assert
    assert lines == f"{cmd.lba} {cmd.value}\n"


def test_write_when_ssd_nand_text_exists(ssd_instance):
    # act
    cmd1 = WriteCommand(cmd="W", lba='2', value='0xAAAABBBB')
    ssd_instance.write(cmd1.lba, cmd1.value)

    cmd2 = WriteCommand(cmd="W", lba='3', value='0xAAAABBBB')
    ssd_instance.write(cmd2.lba, cmd2.value)
    ssd_instance.flush()

    with open(ssd_instance.nand.path, "r") as f:
        line1, line2 = f.readlines()

    # assert
    assert line1 + line2 == f"{cmd1.lba} {cmd1.value}\n{cmd2.lba} {cmd2.value}\n"


def test_write_when_ssd_nand_text_exists_multiple(ssd_instance):
    expected = ""
    for lba in range(100):
        value = f"0x{lba:0{8}x}"
        expected += f"{lba} {value}\n"
        ssd_instance.write(str(lba), value)

    ssd_instance.flush()
    with open(ssd_instance.nand.path, "r") as f:
        result = f.read()

    assert expected == result


def test_write_when_same_lba(ssd_instance):
    # act
    cmd1 = WriteCommand(cmd="W", lba='2', value='0xAAAABBBB')
    ssd_instance.write(cmd1.lba, cmd1.value)

    cmd2 = WriteCommand(cmd="W", lba='2', value='0xFFFFFFFF')
    ssd_instance.write(cmd2.lba, cmd2.value)
    ssd_instance.flush()

    data = dict()
    with open(ssd_instance.nand.path, "r") as f:
        for line in f:
            lba, val = line.rstrip().split(' ')
            data[str(lba)] = val

    # assert
    assert data['2'] == '0xFFFFFFFF'


def test_read_init_value_should_be_0x00000000(ssd_instance):
    """
    기록이 한적이 없는 LBA를 읽으면 0x00000000 으로 읽힌다.
    """
    ssd_instance.read('0')
    data = {}
    with open(ssd_instance.output_writer.output_file, "r") as f:
        for line in f:
            lba, val = line.rstrip().split(' ')
            data[lba] = val

    assert data["0"] == INITIALIZED_DATA


def test_read_creates_ssd_output_text_and_read_value(ssd_instance):
    """
    Read 명령어는 ssd_nand.txt에서 데이터를 읽고,
    읽은 데이터를 ssd_output.txt 파일에 기록한다.
    """
    ssd_instance.write('2', "0xAAAABBBB")
    ssd_instance.flush()
    ssd_instance.read('2')

    data = {}
    with open(ssd_instance.output_writer.output_file, "r") as f:
        for line in f:
            lba, val = line.rstrip().split(' ')
            data[lba] = val

    assert data['2'] == "0xAAAABBBB"


def test_read_origin_ssd_output_should_be_gone(ssd_instance):
    """
    ssd_output.txt 에 읽은 값이 적힌다. (기존 데이터는 사라진다.)
    """
    ssd_instance.write('2', "0xAAAABBBB")
    ssd_instance.read('2')
    ssd_instance.read('3')

    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()

    assert actual != "0xAAAABBBB"


def test_read_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99(ssd_instance):
    """
    잘못된 LBA 범위가 입력되면ssd_output.txt에 ERROR가 기록된다.
    """
    ssd_instance.read('-1')
    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()

    assert actual == ERROR


def test_write_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99(ssd_instance):
    """
     • 잘못된LBA 범위가입력되면ssd_output.txt에 ERROR가 기록된다.
    """
    ssd_instance.write('-1', "0xFFFFFFFF")
    ssd_instance.flush()

    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()

    assert actual == ERROR


def test_error_wrong_ssd_output_txt_if_size_not_0_10(ssd_instance):
    ssd_instance.erase('0', "11")
    ssd_instance.flush()

    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()

    assert actual == ERROR


@pytest.mark.parametrize(
    "lba, size",
    [
        ('91', '10'),
        ('96', '10'),
        ('0', '-2'),
    ]
)
def test_erase_error_wrong_ssd_output_txt_if_lba_size_exceed_99_or_under_0(ssd_instance, lba, size):
    ssd_instance.erase(lba, size)
    ssd_instance.flush()

    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()
    assert actual == ERROR


def test_erase_success(ssd_instance):
    ssd_instance.erase('2', '4')
    ssd_instance.flush()

    with open(ssd_instance.nand.path, "r") as f:
        actual = f.read()

    assert actual == f"2 {INITIALIZED_DATA}\n3 {INITIALIZED_DATA}\n4 {INITIALIZED_DATA}\n5 {INITIALIZED_DATA}\n"


def test_erase_error_on_negative_size(ssd_instance):
    ssd_instance.erase('0', '-1')
    with open(ssd_instance.output_writer.output_file, "r") as f:
        actual = f.read()

    assert actual == f"{ERROR}"


def test_write_and_erase_success(ssd_instance):
    ssd_instance.write('1', '0x12345678')
    ssd_instance.write('2', '0x12345678')
    ssd_instance.erase('2', '4')
    ssd_instance.flush()

    with open(ssd_instance.nand.path, "r") as f:
        actual = f.read()

    assert actual == f"1 0x12345678\n2 {INITIALIZED_DATA}\n3 {INITIALIZED_DATA}\n4 {INITIALIZED_DATA}\n5 {INITIALIZED_DATA}\n"


@pytest.mark.parametrize(
    "lba", ['0', '10', '20', '30', '99']
)
def test_erase_zero_size_success(ssd_instance, lba):
    ssd_instance.erase(lba, '0')
    ssd_instance.flush()

    with pytest.raises(FileNotFoundError):
        with open(ssd_instance.nand.path, "r") as f:
            f.read()
