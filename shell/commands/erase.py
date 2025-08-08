from shell.command import Command
from shell.command_validator import EraseValidator
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 99
ERASE_SIZE = 10

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
        erase_splits = self._split_range(lba, size)
        for split in erase_splits:
            lba_split, size_split = split
            result = self._driver.erase(lba_split, size_split)
            if not result:
                return INVALID_COMMAND
        return DONE

    def _split_range(self, lba: str, size: str):
        start = int(lba)
        size = int(size)
        result = []

        if size > 0:
            while size > 0:
                current_size = min(ERASE_SIZE, size)
                if start + current_size - 1 > LBA_END:
                    current_size = LBA_END - start + 1
                    if current_size <= 0:
                        break
                result.append([str(start), str(current_size)])
                start += current_size
                size -= current_size

        elif size < 0:
            size = -size
            while size > 0:
                current_size = min(ERASE_SIZE, size)
                if start - current_size + 1 < LBA_START:
                    current_size = start - LBA_START + 1
                    if current_size <= 0:
                        break
                start_new = start - current_size + 1
                result.append([str(start_new), str(current_size)])
                start -= current_size
                size -= current_size
        return result
