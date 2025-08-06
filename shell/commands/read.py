from shell.command import Command
from shell.command_validator import ReadValidator
from shell.driver import SSDDriver


class Read(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = ReadValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return "INVALID COMMAND"

        lba = args[0]
        result = self._driver.read(lba)
        return f"[Read] LBA {lba}: {result}"
