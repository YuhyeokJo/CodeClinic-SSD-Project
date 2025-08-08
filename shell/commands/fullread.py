import re

from shell.command_validator import FullReadValidator
from shell.commands.read import Read
from shell.driver import SSDDriver
from shell.command import Command

LBA_MAX = 100
INVALID_COMMAND = "INVALID COMMAND"


class FullRead(Command):
    def __init__(self, driver: SSDDriver):
        self.driver = driver
        self._validator = FullReadValidator()
        self._read = Read(self.driver)

    def excute_multiple_read(self):
        result = ""
        for lba in range(LBA_MAX):
            result += f"\n {self._read.execute([str(lba)])}"
        return result

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
            self.log(result,2)
        else:
            result = self.excute_multiple_read()
            self.log(f"[{self.name}] Done", 2)

        return result
