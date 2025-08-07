import argparse
from pathlib import Path

from shell.command import Command
from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.commands.erase import Erase
from shell.commands.erase_range import EraseRange
from shell.commands.help import Help
from shell.commands.exit import Exit
from shell.commands.script import Script1, Script2, Script3, Script4
from shell.driver import SSDDriver
from shell.logger import Logger

INVALID_COMMAND = "INVALID COMMAND"


class TestShell:
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._commands: dict[str, Command] = {}
        self._register_builtin_commands()
        self._logger = Logger()
        self._logger.print("TestShell.__init__()", f"TEST SHELL START")

    def _register_builtin_commands(self):
        self._commands["write"] = Write(self._driver)
        self._commands["read"] = Read(self._driver)
        self._commands["fullwrite"] = FullWrite(self._driver)
        self._commands["fullread"] = FullRead(self._driver)
        self._commands["erase"] = Erase(self._driver)
        self._commands["erase_range"] = EraseRange(self._driver)
        self._commands["exit"] = Exit(self._driver)
        self._commands["help"] = Help(self._driver)
        self._commands["1_"] = self._commands["1_FullWriteAndReadCompare"] = Script1(self._driver)
        self._commands["2_"] = self._commands["2_PartialLBAWrite"] = Script2(self._driver)
        self._commands["3_"] = self._commands["3_WriteReadAging"] = Script3(self._driver)
        self._commands["4_"] = self._commands["4_EraseAndWriteAging"] = Script4(self._driver)

    def run(self):
        while True:
            line = input("Shell> ").strip()
            if not line:
                print(INVALID_COMMAND)
                self._logger.print("TestShell.run()", INVALID_COMMAND)

                continue
            parts = line.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd not in self._commands:
                print(INVALID_COMMAND)
                self._logger.print("TestShell.run()", INVALID_COMMAND)

                continue

            command = self._commands[cmd]
            command_return = command.execute(args)
            self._logger.print(line, command_return)
            print(command_return)

            if isinstance(command, Exit):
                return

def run_interactive_shell():
    shell = TestShell(SSDDriver())
    shell.run()

def exist_file(file_name: str) -> str:
    if not Path(file_name).exists():
        raise argparse.ArgumentTypeError(f"{file_name}은 존재하지 않는 파일입니다.")
    return file_name

def main():
    parser = argparse.ArgumentParser(description="Shell mode")

    parser.add_argument("script_collection_file_name", nargs='?', type=exist_file)

    args = parser.parse_args()

    if args.script_collection_file_name is None:
        run_interactive_shell()
    else:
        raise NotImplementedError