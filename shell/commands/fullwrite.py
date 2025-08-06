import re

from shell.command import Command
from shell.driver import SSDDriver

LBA_START = 0
LBA_END = 100

FULL_WRITE_DONE = "[Full Write] Done"
INVALLID_COMMAND = "INVALID COMMAND"


class FullWrite(Command):
    def __init__(self, driver:SSDDriver):
        self._driver = driver

    def execute(self, args: list[str]) -> str:
        if len(args) != 1:
            print("Usage: fullwrite <DATA_PATTERN>")
            return INVALLID_COMMAND

        data = args[0]
        if not re.fullmatch(r'0x[0-9A-Fa-f]+', data):
            print("Error: DATA must be a valid hex (0x + 0~9A~F)")
            return INVALLID_COMMAND

        for LBA in range(LBA_START, LBA_END):
            success = self._driver.write(str(LBA), data)
            if not success:
                print(f"Write failed at LBA {LBA}")
                return INVALLID_COMMAND

        return FULL_WRITE_DONE
