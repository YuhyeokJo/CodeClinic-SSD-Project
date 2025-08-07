from command_buffer.command_buffer import CommandBuffer


def test_add_one_command(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "1", "0x12121212")
    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_1_0x12121212\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_three_command(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "2", "0x12121212")
    cb.add_command("W", "3", "0x12121212")
    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_1_0x12121212\n"
                            " - 2_W_2_0x12121212\n"
                            " - 3_W_3_0x12121212\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_more_five_command(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "2", "0x12121212")
    cb.add_command("W", "3", "0x12121212")
    cb.add_command("W", "4", "0x12121212")
    cb.add_command("W", "5", "0x12121212")
    cb.add_command("W", "6", "0x12121212")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_6_0x12121212\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_same_lba_write_command(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "1", "0x12121212")
    cb.add_command("W", "1", "0xAAAAAAAA")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_1_0xAAAAAAAA\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_same_lba_erase_command(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "1", "3")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_3\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_same_lba_more_range_erase_command(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "1", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_5\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_erase_when_write_within_valid_range(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "3", "0x12345678")
    cb.add_command("E", "1", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_5\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_erase_skipped_if_erase_invoked_before_valid_write(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "5")
    cb.add_command("W", "3", "0x12345678")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_5\n"
                            " - 2_W_3_0x12345678\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_when_one_erase_contains_another(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "3", "3")
    cb.add_command("E", "1", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_5\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_when_erases_are_adjacent(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "3")
    cb.add_command("E", "4", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_8\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_when_erases_overlap(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "5")
    cb.add_command("E", "3", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_7\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_rejected_when_resulting_erase_size_exceeds_ten(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "5", "7")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_10\n"
                            " - 2_E_11_1\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_pdf_page30(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "20", "0xABCDABCD")
    cb.add_command("W", "21", "0x12341234")
    cb.add_command("W", "20", "0xEEEEFFFF")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_21_0x12341234\n"
                            " - 2_W_20_0xEEEEFFFF\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_pdf_page31(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "18", "3")
    cb.add_command("W", "21", "0x12341234")
    cb.add_command("E", "18", "5")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_18_5\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_pdf_page32(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "20", "0xABCDABCD")
    cb.add_command("E", "10", "4")
    cb.add_command("E", "12", "3")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_W_20_0xABCDABCD\n"
                            " - 2_E_10_5\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_erases_when_intermediate_erase_added(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "2")
    cb.add_command("E", "4", "4")
    cb.add_command("E", "2", "4")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_7\n"
                            " - 2_empty\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_merge_fails_on_size_limit(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "5")
    cb.add_command("E", "12", "4")
    cb.add_command("E", "5", "8")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_10\n"
                            " - 2_E_11_5\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_erase_merge_with_write_lba_optimization_1(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "10")
    cb.add_command("E", "7", "10")
    cb.add_command("E", "12", "10")
    cb.add_command("W", "11", "0x12345678")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_10\n"
                            " - 2_E_12_10\n"
                            " - 3_W_11_0x12345678\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_erase_merge_with_write_lba_optimization_2(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "10")
    cb.add_command("E", "7", "10")
    cb.add_command("E", "16", "6")
    cb.add_command("W", "11", "0x12345678")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_10\n"
                            " - 2_E_12_10\n"
                            " - 3_W_11_0x12345678\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_write_outside_merged_erase_range_1(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "6", "6")
    cb.add_command("W", "1", "0x12345678")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_2_10\n"
                            " - 2_W_1_0x12345678\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")


def test_write_outside_merged_erase_range_2(capsys):
    cb = CommandBuffer()
    cb.add_command("E", "1", "6")
    cb.add_command("E", "6", "6")
    cb.add_command("W", "11", "0x12345678")

    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == (" - 1_E_1_10\n"
                            " - 2_W_11_0x12345678\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")
