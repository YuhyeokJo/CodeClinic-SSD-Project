import re

from shell.command import Command
from shell.driver import SSDDriver


class FullWrite(Command):
    def __init__(self, driver:SSDDriver):
        self._driver = driver

    def execute(self, args: list[str]) -> None:
        if len(args) != 1:
            print("Usage: fullwrite <DATA_PATTERN>")
            return False

        data = args[0]
        if not re.fullmatch(r'0x[0-9A-Fa-f]+', data):
            print("Error: DATA must be a valid hex (0x + 0~9A~F)")
            return False

        for LBA in range(0, 100):
            success = self._driver.write(str(LBA), data)
            if not success:
                print(f"Write failed at LBA {LBA}")
                return False

        return True
