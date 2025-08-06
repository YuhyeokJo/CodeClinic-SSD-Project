import re
from shell.driver import SSDDriver
from shell.command import Command


class FullRead(Command):
    def __init__(self, driver: SSDDriver):
        self.driver = driver

    def execute(self, arg=None) -> str:
        if arg:
            print("Error: invalid arg.")
            return "INVALID COMMAND"

        result = ""
        for lba in range(100):
            data = self.driver.read(str(lba))
            if not re.fullmatch(r'0x[0-9A-Fa-f]+', data):
                print("Error: DATA must be a valid hex (0x + 0~9A~F)")
                return "INVALID COMMAND"
            result += f"\n [Read] LBA {lba} : {data}"
        return result
