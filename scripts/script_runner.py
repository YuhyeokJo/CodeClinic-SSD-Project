import random
from shell.driver import SSDDriver
from shell.commands.write import Write
from shell.commands.read import Read
from shell.commands.erase import Erase

INVALID_COMMAND = "INVALID COMMAND"
SCRIPT_PASS = "PASS"
SCRIPT_FAIL = "FAIL"


class ScriptRunner:
    def __init__(self, driver: SSDDriver):
        self.seeds = list(range(200))
        self.write_command = Write(driver)
        self.read_command = Read(driver)
        self.erase_command = Erase(driver)

    def full_write_and_read_compare(self) -> str:
        group_size = 5
        inputs = self._make_input_full_write_and_read_compare(group_size)
        groups = [list(inputs.keys())[i * group_size:(i + 1) * group_size] for i in range(100 // group_size)]
        for group in groups:
            for lba in group:
                res = self.write_command.execute([lba, inputs[lba]])
                if INVALID_COMMAND in res:
                    return INVALID_COMMAND
                result = self._read_compare([lba, inputs[lba]])
                if not result:
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
        for _ in range(30):
            for lba in lbas:
                res = self.write_command.execute([lba, value])
                if INVALID_COMMAND in res:
                    return INVALID_COMMAND
            for lba in lbas:
                result = self._read_compare([lba, value])
                if not result:
                    return SCRIPT_FAIL
        return SCRIPT_PASS

    def write_read_aging(self) -> str:
        results = []
        for num_seed in self.seeds:
            random.seed(num_seed)
            value = f"0x{random.randint(0, 0xFFFFFFFF):08X}"
            res = self.write_command.execute(["0", value])
            if INVALID_COMMAND in res:
                return INVALID_COMMAND
            res = self.write_command.execute(["99", value])
            if INVALID_COMMAND in res:
                return INVALID_COMMAND
            result = self._read_compare(["0", value])
            if not result:
                return SCRIPT_FAIL
            result = self._read_compare(["99", value])
            if not result:
                return SCRIPT_FAIL
        return SCRIPT_PASS

    def erase_and_write_aging(self) -> str:
        group_size = 3
        write_data, over_write_data, erased_data = "0x12345678", "0x11112345", "0x00000000"
        self.erase_command.execute(["0", str(group_size)])
        groups = [[str(i), str(i + 1), str(i + 2)] for i in range(2, 97, group_size-1)]
        for _ in range(30):
            for group in groups:
                res = self.write_command.execute([group[0], write_data])
                if INVALID_COMMAND in res:
                    return INVALID_COMMAND
                res = self.write_command.execute([group[0], over_write_data])
                if INVALID_COMMAND in res:
                    return INVALID_COMMAND
                self.erase_command.execute([group[0], str(group_size)])
                for lba in group:
                    result = self._read_compare([lba, erased_data])
                    if not result:
                        return SCRIPT_FAIL
        return SCRIPT_PASS

    def _read_compare(self, args: list[str]) -> bool:
        lba, data = args[0], args[1]
        res = self.read_command.execute([lba])
        if res.split(" ")[-1] != data:
            return False
        return True
