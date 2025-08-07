from shell.command import Command
from shell.command_validator import EraseRangeValidator
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 99

DONE = "[Erase Range] Done"
INVALID_COMMAND = "INVALID COMMAND"


class EraseRange(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = EraseRangeValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALID_COMMAND
        lba_start, lba_end = args
        lba_end = LBA_END if int(lba_end) > LBA_END else lba_end
        result = self._driver.erase_range(lba_start, lba_end)
        if not result:
            return INVALID_COMMAND
        return DONE
