from shell.command import Command
from shell.command_constants import INVALID_COMMAND
from shell.command_validator import ExitValidator
from shell.driver import SSDDriver


class Exit(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = ExitValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
        else:
            result = f"[{self.name}]"
        self.log(result, 1)
        return result
