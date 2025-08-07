import argparse
from dataclasses import dataclass
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


class InteractiveShell:
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


class BatchShellError(Exception):
    """Base error"""


class NotExistingTestScriptError(BatchShellError):
    """Not existing scripts"""


class NotExistingFileError(BatchShellError):
    """Not existing scripts"""


class BatchShell:
    @dataclass
    class Script:
        full_name: str
        command: Command

    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._script_collection_file_path = None
        self._script_list: list[BatchShell.Script] = []
        self._registered_script: dict[str, BatchShell.Script] = {}
        self._register_builtin_script()

    @property
    def script_collection_file_path(self):
        return self._script_collection_file_path

    @script_collection_file_path.setter
    def script_collection_file_path(self, file_path: Path):
        if not file_path.exists():
            raise NotExistingFileError(f"{file_path} does not exist")

        with file_path.open("r") as f:
            for line in f.readlines():
                line = line.strip("\n")
                if line in self._registered_script:
                    self._script_list.append(self._registered_script[line])
                else:
                    raise NotExistingTestScriptError(f"{line} is not registered test script")

        self._script_collection_file_path = file_path

    def _run_script(self, script: Script):
        result = script.command.execute([])
        return result == "PASS"

    def run(self):
        for script in self._script_list:
            print(f"{script.full_name}  ___  Run...", end="", flush=True)
            if self._run_script(script):
                print("Pass", flush=True)
            else:
                print("Fail", flush=True)

    def _register_builtin_script(self):
        self._registered_script["1_"] = self._registered_script["1_FullWriteAndReadCompare"] \
            = BatchShell.Script("1_FullWriteAndReadCompare", Script1(self._driver))

        self._registered_script["2_"] = self._registered_script["2_PartialLBAWrite"] \
            = BatchShell.Script("2_PartialLBAWrite", Script2(self._driver))

        self._registered_script["3_"] = self._registered_script["3_WriteReadAging"] \
            = BatchShell.Script("3_WriteReadAging", Script3(self._driver))

        self._registered_script["4_"] = self._registered_script["4_EraseAndWriteAging"] \
            = BatchShell.Script("4_EraseAndWriteAging", Script4(self._driver))


def run_interactive_shell():
    shell = InteractiveShell(SSDDriver())
    shell.run()


def exist_file(file_name: str) -> str:
    if not Path(file_name).exists():
        raise argparse.ArgumentTypeError(f"{file_name}은 존재하지 않는 파일입니다.")
    return file_name


def run_batch_shell(file_name: str):
    shell = BatchShell(SSDDriver())
    shell.script_collection_file_path = Path(file_name)
    shell.run()


def main():
    parser = argparse.ArgumentParser(description="Shell mode")

    parser.add_argument("script_collection_file_name", nargs='?', type=exist_file)

    args = parser.parse_args()

    if args.script_collection_file_name is None:
        run_interactive_shell()
    else:
        run_batch_shell(args.script_collection_file_name)
