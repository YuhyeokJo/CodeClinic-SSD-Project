from shell.command import Command
from shell.command_validator import EraseValidator
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 100

DONE = "[Erase] Done"
INVALID_COMMAND = "INVALID COMMAND"


class Erase(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = EraseValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALID_COMMAND
        lba, size = args

        result = self._driver.erase(lba, size)
        if not result:
            return INVALID_COMMAND
        return DONE
