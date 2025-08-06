from pathlib import Path
from device import Device
import os
import argparse

INITIALIZED_DATA = "0x00000000"


class SSD(Device):
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.ssd_nand_file = self.output_dir / "ssd_nand.txt"
        self.ssd_output_file = self.output_dir / "ssd_output.txt"

    def write(self, lba: int, value: int | str) -> None:
        if lba < 0 or 99 < lba:
            with open(self.ssd_output_file, "w") as f:
                f.write("ERROR")
            return

        data = self._load_nand_data()
        data[str(lba)] = value if isinstance(value, str) else hex(value)
        self._save_nand_data(data)

    def read(self, lba: int) -> None:
        if lba < 0 or 99 < lba:
            with open(self.ssd_output_file, "w") as f:
                f.write("ERROR")
            return

        data = self._load_nand_data()
        result = data.get(lba, INITIALIZED_DATA)
        with open(self.ssd_output_file, "w") as f:
            f.write(f"{lba} {result}\n")

    def _load_nand_data(self) -> dict:
        data = {}
        if os.path.exists(self.ssd_nand_file):
            with open(self.ssd_nand_file, "r") as f:
                for line in f:
                    lba, val = line.rstrip().split()
                    data[lba] = val
        return data

    def _save_nand_data(self, data: dict) -> None:
        with open(self.ssd_nand_file, "w") as f:
            for lba, val in sorted(data.items()):
                f.write(f"{lba} {val}\n")


def main():
    parser = argparse.ArgumentParser(description="SSD command")
    subparsers = parser.add_subparsers(dest="command", help="")

    write_parser = subparsers.add_parser("W", help="Write")
    write_parser.add_argument("lba", type=int)
    write_parser.add_argument("value", type=str, help="Value to write")

    read_parser = subparsers.add_parser("R", help="Read")
    read_parser.add_argument("lba", type=int, help="LBA to read from")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        exit(1)

    ssd = SSD()
    if args.command == "W":
        ssd.write(args.lba, args.value)
    elif args.command == "R":
        ssd.read(args.lba)


if __name__ == "__main__":
    main()
