import pytest
import shutil

from dataclasses import dataclass

from pytest_mock import MockerFixture

from device import ssd
from device.ssd import SSD


@dataclass
class WriteCommand:
    cmd: str
    address: int
    value: int | str


@pytest.fixture
def ssd_instance():
    ssd_instance = SSD()
    shutil.rmtree(ssd_instance.output_dir, ignore_errors=True)
    return SSD()


def test_main_write_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    mock_args = mocker.Mock(command='W', lba=10, value='0xABCDEF01')
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_args)

    ssd.main()

    mock_ssd.write.assert_called_once_with(10, '0xABCDEF01')
    mock_ssd.read.assert_not_called()


def test_main_read_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    mock_args = mocker.Mock(command='R', lba=10)
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_args)

    ssd.main()

    mock_ssd.read.assert_called_once_with(10)
    mock_ssd.write.assert_not_called()


def test_main_other_command(ssd_instance, mocker: MockerFixture):
    mock_ssd = mocker.Mock(spec=SSD)
    mocker.patch('device.ssd.SSD', return_value=mock_ssd)
    mock_args = mocker.Mock(command='K', lba=10)
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_args)

    ssd.main()

    mock_ssd.read.assert_not_called()
    mock_ssd.write.assert_not_called()


def test_write_when_no_ssd_nand_text_create_then_write(ssd_instance):
    """
    ssd_nand.txt 파일이 없는 경우, 생성 후 데이터가 기록되어야 한다.
    """
    # arrange
    cmd = WriteCommand(cmd="W", address=2, value=0xAAAABBBB)

    # act
    ssd_instance.write(cmd.address, cmd.value)

    with open(ssd_instance.ssd_nand_file, "r") as f:
        lines = f.readlines()[0]

    # assert
    assert lines == f"{cmd.address} {hex(cmd.value)}\n"


def test_write_when_ssd_nand_text_exists(ssd_instance):
    # act
    cmd1 = WriteCommand(cmd="W", address=2, value=0xAAAABBBB)
    ssd_instance.write(cmd1.address, cmd1.value)

    cmd2 = WriteCommand(cmd="W", address=3, value=0xAAAABBBB)
    ssd_instance.write(cmd2.address, cmd2.value)

    with open(ssd_instance.ssd_nand_file, "r") as f:
        line1, line2 = f.readlines()

    # assert
    assert line1 + line2 == f"{cmd1.address} {hex(cmd1.value)}\n{cmd2.address} {hex(cmd2.value)}\n"


def test_write_when_same_address(ssd_instance):
    # act
    cmd1 = WriteCommand(cmd="W", address=2, value=0xAAAABBBB)
    ssd_instance.write(cmd1.address, cmd1.value)

    cmd2 = WriteCommand(cmd="W", address=2, value=0xFFFFFFFF)
    ssd_instance.write(cmd2.address, cmd2.value)

    data = dict()
    with open(ssd_instance.ssd_nand_file, "r") as f:
        for line in f:
            address, val = line.rstrip().split(' ')
            data[str(address)] = val

    # assert
    assert data['2'] == '0xffffffff'


def test_read_init_value_should_be_0x00000000(ssd_instance):
    """
    기록이 한적이 없는 LBA를 읽으면 0x00000000 으로 읽힌다.
    """
    ssd_instance.read(0)
    data = {}
    with open(ssd_instance.ssd_output_file, "r") as f:
        for line in f:
            address, val = line.rstrip().split(' ')
            data[address] = val

    assert data["0"] == "0x00000000"


def test_read_creates_ssd_output_text_and_read_value(ssd_instance):
    """
    Read 명령어는 ssd_nand.txt에서 데이터를 읽고,
    읽은 데이터를 ssd_output.txt 파일에 기록한다.
    """
    pytest.fail()


def test_read_origin_ssd_output_should_be_gone(ssd_instance):
    """
     ssd_output.txt 에 읽은 값이 적힌다. (기존 데이터는 사라진다.)
    """
    pytest.fail()

def test_read_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99(ssd_instance):
    """
     • 잘못된LBA 범위가 입력되면ssd_output.txt에 "ERROR"가 기록된다.
    """
    ssd_instance.read(-1)
    with open(ssd_instance.ssd_output_file, "r") as f:
        actual = f.readlines()[0]

    assert actual == "ERROR"


def test_write_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99(ssd_instance):
    """
     • 잘못된LBA 범위가입력되면ssd_output.txt에 "ERROR"가 기록된다.
    """
    ssd_instance.write(-1, "0xffffffff")
    with open(ssd_instance.ssd_output_file, "r") as f:
        actual = f.readlines()[0]

    assert actual == "ERROR"


def test_lba_should_be_decimal(ssd_instance):
    """
    • [LBA] : 0 ~ 99, 10진수로 입력 받음
    """

    pytest.fail()


def test_value_always_startswith_0x_and_length_10(ssd_instance):
    """
    [Value] : 항상 0x가 붙으며 10 글자로 표기한다. ( 0x00000000  ~  0xFFFFFFFF)
    """
    pytest.fail()
