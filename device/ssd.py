from pathlib import Path
from device.device import Device
import os


class SSD(Device):
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.ssd_nand_file = self.output_dir / "ssd_nand.txt"
        self.ssd_output_file = self.output_dir / "ssd_output.txt"

    def write(self, address: int | str, value: int | str):
        data = {}
        if os.path.exists(self.ssd_nand_file):
            with open(self.ssd_nand_file, "r") as f:
                for line in f:
                    addr, val = line.rstrip().split()
                    data[str(addr)] = val
        data[str(address)] = value if isinstance(value, str) else hex(value)

        with open(self.ssd_nand_file, "w") as f:
            for addr, val in sorted(data.items()):
                f.write(f"{addr} {val}\n")

    def read(self, address):
        data = {}
        if os.path.exists(self.ssd_nand_file):
            with open(self.ssd_nand_file, "r") as f:
                for line in f:
                    addr, val = line.rstrip().split()
                    data[str(addr)] = val

        result = data.get(address, "0x00000000")
        with open(self.ssd_output_file, "w") as f:
            f.write(f"{address} {result}\n")
