from shell.command import Command
from shell.command_constants import INVALID_COMMAND, LBA_START, LBA_MAX, ERASE_SIZE
from shell.command_validator import EraseValidator
from shell.driver import SSDDriver


class Erase(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = EraseValidator()

    def execute_multiple_erase(self, erase_splits):
        for split in erase_splits:
            lba_split, size_split = split
            result = self._driver.erase(lba_split, size_split)
            if not result:
                return f"[{self.name}] Fail"
        return f"[{self.name}] Done"

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
        else:
            lba, size = args
            erase_splits = self._split_range(lba, size)
            result = self.execute_multiple_erase(erase_splits)

        self.log(result, 3)
        return result

    def _split_range(self, lba: str, size: str):
        start = int(lba)
        size = int(size)
        result = []

        if size > 0:
            while size > 0:
                current_size = min(ERASE_SIZE, size)
                if start + current_size - 1 > LBA_MAX:
                    current_size = LBA_MAX - start + 1
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
