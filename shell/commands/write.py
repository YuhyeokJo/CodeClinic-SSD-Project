import subprocess

from shell.command import Command
from shell.driver import SSDDriver


class WriteCommand(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver

    def execute(self, args: list[str]) -> str:
        if len(args) != 2:
            return "INVALID COMMAND"
        lba, data = args
        try:
            int(lba)
        except:
            return "INVALID COMMAND"

        if not 0 <= int(lba) <= 99:
            return "INVALID COMMAND"

        if len(data) != 10:
            return "INVALID COMMAND"

        prefix, hex_digit = data[:2], data[2:]
        if prefix != "0x":
            return "INVALID COMMAND"
        for d in hex_digit:
            if not d.isdigit() and not d in ["A", "B", "C", "D", "E", "F"]:
                return "INVALID COMMAND"

        result = self._driver.write(lba, data)
        if not result:
            return "INVALID COMMAND"
        else:
            return f"[Write] Done"