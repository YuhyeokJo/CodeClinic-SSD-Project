from pathlib import Path
from device import Device
import os
import argparse


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


if "__main__" == __name__:
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
        print(f"{args.command=}, {args.lba=}, {args.value=}")
        ssd.write(str(args.lba), args.value)
    elif args.command == "R":
        print(f"{args.command=}, {args.lba=}")
        ssd.read(str(args.lba))
