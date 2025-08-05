from shell.command import Command
from shell.driver import SSDDriver


class FullWrite(Command):
    def __init__(self, driver:SSDDriver):
        self._driver = driver

    def execute(self, args: list[str]) -> None:
        for LBA in range(0, 99):
            self._driver.write(str(LBA), args[0])
        return True
