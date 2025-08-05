from shell.commands.fullwrite import FullWrite


def test_full_write_command():
    full_write_command = FullWrite()
    assert full_write_command.execute(['fullwrite 0xABCDFFFF'])