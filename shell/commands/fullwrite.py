import re

from shell.command import Command
from shell.command_validator import FullWriteValidator
from shell.commands.write import Write
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 100

FULL_WRITE_DONE = "[Full Write] Done"
INVALLID_COMMAND = "INVALID COMMAND"


class FullWrite(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = FullWriteValidator()
        self._write = Write(self._driver)

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALLID_COMMAND

        data = args[0]

        for LBA in range(LBA_START, LBA_END):
            if self._write.execute([str(LBA), data]) == INVALLID_COMMAND:
                return INVALLID_COMMAND

        return FULL_WRITE_DONE
