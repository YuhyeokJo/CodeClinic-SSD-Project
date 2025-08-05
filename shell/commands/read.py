from shell.command import Command
from shell.driver import SSDDriver


class ReadCommand(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver

    def execute(self, args: list[str])->str:
        if len(args) != 1:
            print("Usage: read <LBA>")
            return "[READ] INVALID COMMAND"

        if not args[0].isdigit():
            print("LBA must be a number")
            return "[READ] INVALID COMMAND"

        lba = args[0]
        result = self._driver.read(lba)
        return f"[READ] LBA {lba}: {result}"
