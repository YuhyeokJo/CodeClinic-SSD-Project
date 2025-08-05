from pathlib import Path
from device.device import Device


class SSD(Device):
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.ssd_nand_file = self.output_dir / "ssd_nand.txt"

    def write(self, cmd, address, value):
        with open(self.ssd_nand_file, "w") as f:
            f.writelines(f"{address} {hex(value)}\n")

    def read(self, cmd, address):
        pass
