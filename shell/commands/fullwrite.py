from shell.command import Command
from shell.command_constants import INVALID_COMMAND, LBA_START, LBA_END
from shell.command_validator import FullWriteValidator
from shell.commands.write import Write
from shell.driver import SSDDriver


class FullWrite(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = FullWriteValidator()
        self._write = Write(self._driver)

    def execute_multiple_write(self, data):
        for LBA in range(LBA_START, LBA_END):
            if self._write.execute([str(LBA), data]) == INVALID_COMMAND:
                return INVALID_COMMAND
        return f"[{self.name}] Done"

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
        else:
            result = self.execute_multiple_write(args[0])

        self.log(result, 2)
        return result
