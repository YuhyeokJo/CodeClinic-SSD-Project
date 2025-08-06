from shell.command import Command
from shell.driver import SSDDriver


class Read(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver

    def execute(self, args: list[str])->str:
        if len(args) != 1:
            print("Usage: read <LBA>")
            return "[Read] INVALID COMMAND"

        if not args[0].isdigit():
            print("LBA must be a number")
            return "[Read] INVALID COMMAND"

        lba = args[0]
        result = self._driver.read(lba)
        return f"[Read] LBA {lba}: {result}"
