from shell.command import Command
from shell.command_validator import EraseRangeValidator
from shell.commands.erase import Erase
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 99

DONE = "[Erase Range] Done"
INVALID_COMMAND = "INVALID COMMAND"


class EraseRange(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = EraseRangeValidator()
        self._erase = Erase(self._driver)

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALID_COMMAND
        lba_start, lba_end = args
        size = self._get_size(lba_end, lba_start)
        result = self._erase.execute([lba_start, size])
        if not result:
            return INVALID_COMMAND
        return DONE

    def _get_size(self, lba_end, lba_start):
        diff = int(lba_end) - int(lba_start)
        if diff > 0:
            size = str(diff + 1)
        elif diff < 0:
            size = str(diff - 1)
        else:
            size = str(0)
        return size
