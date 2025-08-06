import re

from shell.command_validator import FullReadValidator
from shell.driver import SSDDriver
from shell.command import Command


class FullRead(Command):
    def __init__(self, driver: SSDDriver):
        self.driver = driver
        self._validator = FullReadValidator()

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return "INVALID COMMAND"

        result = ""
        for lba in range(100):
            data = self.driver.read(str(lba))
            result += f"\n [Read] LBA {lba}: {data}"
        return result
