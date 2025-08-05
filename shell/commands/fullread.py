from shell.driver import SSDDriver
from shell.command import Command

class Fullread(Command):
    def __init__(self, driver: SSDDriver):
        self.driver = driver

    def execute(self, arg=None) -> str:
        result = ""
        for lba in range(100):
            result += f"\n [Write] LBA {lba} : {self.driver.read(str(lba))}"
        return result
