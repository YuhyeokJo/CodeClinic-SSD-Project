from shell.command import Command

class FullWrite(Command):
    def execute(self, args: list[str]) -> None:
        return True