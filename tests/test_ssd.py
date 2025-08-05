import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from device.ssd import SSD


def test_write_when_no_ssd_nand_text_create_then_write():
    """
    ssd_nand.txt 파일이 없는 경우, 생성 후 데이터가 기록되어야 한다.
    """
    ssd = SSD()
    Path(ssd.ssd_nand_file).unlink()
    cmd = "W"
    address = 2
    value = 0xAAAABBBB
    ssd.write(cmd, address, value)

    with open(ssd.ssd_nand_file, "r") as f:
        lines = f.readlines()[0]

    assert lines == f"{address} {hex(value)}\n"


def test_write_when_ssd_nand_text_exists():
    """
    write 명령어시 ssd_nand.txt 파일에 값을 저장 해 둔다
    """


def test_read_creates_ssd_output_text_and_read_value():
    """
    write 명령어시 ssd_nand.txt 파일에 값을 저장 해 둔다
    ssd_nand.txt 파일이 없는 경우, 생성 후 데이터가 기록되어야 한다.
    """
    ...


def test_read_output_should_be_gone():
    """
     ssd_output.txt 에 읽은 값이 적힌다. (기존 데이터는 사라진다.)
    """
    ...


def test_read_init_value_should_be_0x00000000():
    """
    기록이 한적이 없는 LBA를 읽으면 0x00000000 으로 읽힌다.
    """
    ...


def test_read_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99():
    """
     • 잘못된LBA 범위가 입력되면ssd_output.txt에 "ERROR"가 기록된다.
    """
    ...


def test_write_wrong_lba_print_ERROR_at_ssd_output_txt_if_not_0_99():
    """
     • 잘못된LBA 범위가입력되면ssd_output.txt에 "ERROR"가 기록된다.
    """
    ...


def test_lba_should_be_decimal():
    """
    • [LBA] : 0 ~ 99, 10진수로 입력 받음
    """
    ...


def test_value_always_startswith_0x_and_length_10():
    """
    [Value] : 항상 0x가 붙으며 10 글자로 표기한다. ( 0x00000000  ~  0xFFFFFFFF)
    """
    ...
