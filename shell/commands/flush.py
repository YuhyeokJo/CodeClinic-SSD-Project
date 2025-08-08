from shell.command import Command
from shell.command_constants import INVALID_COMMAND
from shell.command_validator import FlushValidator
from shell.driver import SSDDriver

FLUSH_DONE = "[Flush] Done"


class Flush(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = FlushValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return INVALID_COMMAND
        result = self._driver.flush()
        if not result:
            return INVALID_COMMAND
        return FLUSH_DONE
