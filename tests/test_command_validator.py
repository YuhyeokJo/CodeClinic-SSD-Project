import pytest

from shell.command_validator import is_valid_lba

@pytest.mark.parametrize(
    "correct_string", ["1", "01", "11"]
)
def test_if_lba_validate_correct_number(correct_string):
    assert is_valid_lba(correct_string) == True

@pytest.mark.parametrize(
    "wrong_string", ["-1", "1.0", "100", "①②③"]
)
def test_if_lba_validate_wrong_number_as_false(wrong_string):
    assert is_valid_lba(wrong_string) == False