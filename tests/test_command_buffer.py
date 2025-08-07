from command_buffer.command_buffer import CommandBuffer


def test_add_one_command(capsys):
    cb = CommandBuffer()
    cb.add_command("W", "1", "0x12121212")
    cb.show_status()
    captured = capsys.readouterr()
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_W_1_0x12121212\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_W_1_0x12121212\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_W_6_0x12121212\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_W_1_0xAAAAAAAA\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_E_1_3\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_E_1_5\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_E_1_5\n"
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
    assert captured.out == ("=== Buffer 상태 ===\n"
                            " - 1_W_3_0x12345678\n"
                            " - 2_E_1_5\n"
                            " - 3_empty\n"
                            " - 4_empty\n"
                            " - 5_empty\n")
