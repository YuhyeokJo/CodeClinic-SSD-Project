from device import CommandBuffer


def test_add_one_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "1", "0x12121212")

    assert cb.show_status() == ["1_W_1_0x12121212",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_three_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "2", "0x12121212")
    cb.add_command("W", "3", "0x12121212")

    cb.show_status()
    assert cb.show_status() == ["1_W_1_0x12121212",
                                "2_W_2_0x12121212",
                                "3_W_3_0x12121212",
                                "4_empty",
                                "5_empty"]


def test_more_five_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "2", "0x12121212")
    cb.add_command("W", "3", "0x12121212")
    cb.add_command("W", "4", "0x12121212")
    cb.add_command("W", "5", "0x12121212")
    cb.add_command("W", "6", "0x12121212")

    cb.show_status()
    assert cb.show_status() == ["1_W_6_0x12121212",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_same_lba_write_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "1", "0xAAAAAAAA")

    assert cb.show_status() == ["1_W_1_0xAAAAAAAA",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_same_lba_erase_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "1", "3")

    assert cb.show_status() == ["1_E_1_3",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_same_lba_more_range_erase_command():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "1", "5")

    assert cb.show_status() == ["1_E_1_5",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_erase_when_write_within_valid_range():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "3", "0x12345678")
    cb.add_command("E", "1", "5")

    assert cb.show_status() == ["1_E_1_5",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_erase_skipped_if_erase_invoked_before_valid_write():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "5")
    cb.add_command("W", "3", "0x12345678")

    assert cb.show_status() == ["1_E_1_5",
                                "2_W_3_0x12345678",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_when_one_erase_contains_another():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "3", "3")
    cb.add_command("E", "1", "5")

    assert cb.show_status() == ["1_E_1_5",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_when_erases_are_adjacent():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "4", "5")

    assert cb.show_status() == ["1_E_1_8",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_when_erases_overlap():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "5")
    cb.add_command("E", "3", "5")

    assert cb.show_status() == ["1_E_1_7",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_rejected_when_resulting_erase_size_exceeds_ten():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "5", "7")

    assert cb.show_status() == ["1_E_1_10",
                                "2_E_11_1",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_pdf_page30():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "20", "0xABCDABCD")
    cb.add_command("W", "21", "0x12341234")
    cb.add_command("W", "20", "0xEEEEFFFF")

    assert cb.show_status() == ["1_W_21_0x12341234",
                                "2_W_20_0xEEEEFFFF",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_pdf_page31():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "18", "3")
    cb.add_command("W", "21", "0x12341234")
    cb.add_command("E", "18", "5")

    assert cb.show_status() == ["1_E_18_5",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_pdf_page32():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("W", "20", "0xABCDABCD")
    cb.add_command("E", "10", "4")
    cb.add_command("E", "12", "3")

    assert cb.show_status() == ["1_W_20_0xABCDABCD",
                                "2_E_10_5",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_erases_when_intermediate_erase_added():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "2")
    cb.add_command("E", "4", "4")
    cb.add_command("E", "2", "4")

    assert cb.show_status() == ["1_E_1_7",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_merge_fails_on_size_limit():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "5")
    cb.add_command("E", "12", "4")
    cb.add_command("E", "5", "8")

    assert cb.show_status() == ["1_E_1_10",
                                "2_E_11_5",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_erase_merge_with_write_lba_optimization_1():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "10")
    cb.add_command("E", "7", "10")
    cb.add_command("E", "12", "10")
    cb.add_command("W", "11", "0x12345678")

    assert cb.show_status() == ["1_E_1_10",
                                "2_E_12_10",
                                "3_W_11_0x12345678",
                                "4_empty",
                                "5_empty"]


def test_erase_merge_with_write_lba_optimization_2():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "10")
    cb.add_command("E", "7", "10")
    cb.add_command("E", "16", "6")
    cb.add_command("W", "11", "0x12345678")

    assert cb.show_status() == ["1_E_1_10",
                                "2_E_12_10",
                                "3_W_11_0x12345678",
                                "4_empty",
                                "5_empty"]


def test_write_outside_merged_erase_range_1():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "6", "6")
    cb.add_command("W", "1", "0x12345678")

    assert cb.show_status() == ["1_E_2_10",
                                "2_W_1_0x12345678",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_write_outside_merged_erase_range_2():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "6", "6")
    cb.add_command("W", "11", "0x12345678")

    assert cb.show_status() == ["1_E_1_10",
                                "2_W_11_0x12345678",
                                "3_empty",
                                "4_empty",
                                "5_empty"]


def test_write_invalidated_by_later_duplicate_erase():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "10")
    cb.add_command("W", "5", "0x12345678")
    cb.add_command("E", "1", "10")

    assert cb.show_status() == ["1_E_1_10",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]

def test_erase_removes_previous_write_within_range():
    cb = CommandBuffer()
    cb.initialize_buffer()
    cb.add_command("E", "1", "10")
    cb.add_command("W", "5", "0x12345678")
    cb.add_command("E", "1", "9")

    assert cb.show_status() == ["1_E_1_10",
                                "2_empty",
                                "3_empty",
                                "4_empty",
                                "5_empty"]