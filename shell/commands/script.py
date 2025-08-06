from shell.command import Command
from shell.driver import SSDDriver
from scripts.script_runner import ScriptRunner


class Script1(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        return self.script_runner.full_write_and_read_compare()


class Script2(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        return self.script_runner.scenario2()


class Script3(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        return self.script_runner.scenario3()
