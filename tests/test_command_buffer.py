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
