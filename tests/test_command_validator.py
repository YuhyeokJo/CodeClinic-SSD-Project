import pytest

from shell.command_validator import is_valid_lba

def test_if_lba_validate_correct_number():
    assert is_valid_lba("1") == True
    assert is_valid_lba("01") == True
    assert is_valid_lba("11") == True

def test_if_lba_validate_wrong_number_as_false():
    assert is_valid_lba("-1") == False
    assert is_valid_lba("1.0") == False
    assert is_valid_lba("100") == False

def test_if_lba_validate_unicode_number_as_false():
    assert is_valid_lba("①②③") == False