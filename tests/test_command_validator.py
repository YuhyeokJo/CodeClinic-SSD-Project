import pytest

from shell.command_validator import is_valid_lba, LBA_RANGE


@pytest.mark.parametrize(
    "correct_string", [str(i) for i in LBA_RANGE]
)
def test_if_lba_validate_correct_number(correct_string):
    assert is_valid_lba(correct_string) == True


@pytest.mark.parametrize(
    "wrong_string", [
        "-1", "100",  # 정수지만, 범위 외
        "00", "01", "1.0", "00011",  # 범위 내 정수지만, 틀린 포맷
        "①②"  # 범위 내 정수지만, 유니 코드
    ]
)
def test_if_lba_validate_wrong_number_as_false(wrong_string):
    assert is_valid_lba(wrong_string) == False
