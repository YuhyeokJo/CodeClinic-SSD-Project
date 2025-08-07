from shell.command import Command
from shell.command_validator import EraseRangeValidator
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 100

DONE = "[Erase range] Done"
INVALID_COMMAND = "INVALID COMMAND"


class EraseRange(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = EraseRangeValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALID_COMMAND
        start_lba, end_lba = args

        result = self._driver.erase_range(start_lba, end_lba)
        if not result:
            return INVALID_COMMAND
        return DONE
