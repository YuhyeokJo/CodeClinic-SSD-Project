import re

from shell.command_validator import FullReadValidator
from shell.commands.read import Read
from shell.driver import SSDDriver
from shell.command import Command

INVALID_COMMAND = "INVALID COMMAND"


class FullRead(Command):
    def __init__(self, driver: SSDDriver):
        self.driver = driver
        self._validator = FullReadValidator()
        self._read = Read(self.driver)

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
            self.log(result)

        else:
            result = ""
            for lba in range(100):
                result += f"\n {self._read.execute([str(lba)])}"
            self.log(f"[{self.name}] Done")

        return result
