from shell.driver import SSDDriver
from shell.commands.write import Write
from shell.commands.read import Read

INVALID = "INVALID"
SCRIPT_INVALID_COMMAND = "[SCRIPT] INVALID COMMAND"
SCRIPT_PASS = "[SCRIPT] PASS"
SCRIPT_FAIL = "[SCRIPT] FAIL"


class ScriptRunner:
    def __init__(self, driver: SSDDriver):
        self.write_command = Write(driver)
        self.read_command = Read(driver)

    def full_write_and_read_compare(self) -> str:
        results = []
        group_size = 5
        inputs = self._make_input_full_write_and_read_compare(group_size)
        groups = [list(inputs.keys())[i * group_size:(i + 1) * group_size] for i in range(100 // group_size)]
        for group in groups:
            for lba in group:
                res = self.write_command.execute([lba, inputs[lba]])
                if INVALID in res:
                    return SCRIPT_INVALID_COMMAND
                results.append(self._read_compare([lba, inputs[lba]]))
        print(results)
        if not all(results):
            return SCRIPT_FAIL
        return SCRIPT_PASS

    def _make_input_full_write_and_read_compare(self, group_size):
        inputs = {}
        base_value = 0x12345678
        values = [f"0x{base_value + i * 0x10:X}" for i in range(100 // group_size)]
        for i in range(100):
            key = str(i)
            value = values[i // group_size]
            inputs[key] = value
        return inputs

    def scenario2(self) -> str:
        pass

    def scenario3(self) -> str:
        pass

    def _read_compare(self, args: list[str]) -> bool:
        lba, data = args[0], args[1]
        res = self.read_command.execute([lba])
        print(res)
        if res.split(" ")[-1] != data:
            return False
        return True
