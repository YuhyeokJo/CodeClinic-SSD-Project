from shell.command import Command
from shell.command_validator import ExitValidator
from shell.driver import SSDDriver

INVALID_COMMAND = "INVALID COMMAND"


class Exit(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = ExitValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            result = INVALID_COMMAND
        else:
            result = f"[{self.name}]"
        return result
