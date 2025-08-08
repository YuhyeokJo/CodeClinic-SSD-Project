from shell.command import Command
from shell.command_validator import ReadValidator
from shell.driver import SSDDriver

INVALID_COMMAND = "INVALID COMMAND"


class Read(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = ReadValidator()
        self._name = 'Read'

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
        else:
            lba = args[0]
            result = f"[Read] LBA {lba}: {self._driver.read(lba)}"

        self.log(self._name, result)
        return result
