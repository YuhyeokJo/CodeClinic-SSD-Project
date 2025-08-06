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

    def partial_lba_write(self) -> str:
        value = "0x11112345"
        lbas = ["4", "0", "3", "1", "2"]
        results = []
        for _ in range(30):
            for lba in lbas:
                res = self.write_command.execute([lba, value])
                if INVALID in res:
                    return SCRIPT_INVALID_COMMAND
            for lba in lbas:
                results.append(self._read_compare([lba, value]))
        if not all(results):
            return SCRIPT_FAIL
        return SCRIPT_PASS

    def write_read_aging(self) -> str:
        pass

    def _read_compare(self, args: list[str]) -> bool:
        lba, data = args[0], args[1]
        res = self.read_command.execute([lba])
        if res.split(" ")[-1] != data:
            return False
        return True
