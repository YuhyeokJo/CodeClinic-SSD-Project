from shell.command import Command
from shell.driver import SSDDriver


class Help(Command):
    def __init__(self, driver:SSDDriver):
        self._driver = driver

    def execute(self, args: list[str]) -> str:
        # self._driver.close()
        return "[Help]"
