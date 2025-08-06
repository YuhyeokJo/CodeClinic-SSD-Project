import subprocess

from shell.command import Command
from shell.command_validator import WriteValidator
from shell.driver import SSDDriver


class Write(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = WriteValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return "INVALID COMMAND"
        lba, data = args

        result = self._driver.write(lba, data)
        if not result:
            return "INVALID COMMAND"
        else:
            return f"[Write] Done"
