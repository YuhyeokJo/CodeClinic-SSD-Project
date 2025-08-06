import re

from shell.command import Command
from shell.command_validator import FullWriteValidator
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 100

FULL_WRITE_DONE = "[Full Write] Done"
INVALLID_COMMAND = "INVALID COMMAND"

class FullWrite(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = FullWriteValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALLID_COMMAND

        data = args[0]

        for LBA in range(LBA_START, LBA_END):
            success = self._driver.write(str(LBA), data)
            if not success:
                return INVALLID_COMMAND

        return FULL_WRITE_DONE
