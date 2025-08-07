import subprocess
from pathlib import Path


class SSDDriver:
    def read(self, lba: str):
        subprocess.run(
            f"python {Path(__file__).parent.parent/'device/ssd.py'} R {lba}",
            shell=True
        )

        output_dir = Path(__file__).resolve().parent.parent / "output"
        ssd_output_file = output_dir / "ssd_output.txt"

        with open(ssd_output_file, "r") as f:
            val = f.readline().rstrip().split()[1]
            return val

    def write(self, lba: str, data: str):
        subprocess.run(
            f"python {Path(__file__).parent.parent/'device/ssd.py'} W {lba} {data}",
            shell=True
        )

        return True

    def erase(self, lba: str, size: str):
        subprocess.run(
            f"python {Path(__file__).parent.parent / 'device/ssd.py'} E {lba} {size}",
            shell=True
        )

        return True

    def erase_range(self, start_lba: str, end_lba: str):
        size = int(end_lba) - int(start_lba) + 1
        subprocess.run(
            f"python {Path(__file__).parent.parent / 'device/ssd.py'} E {start_lba} {str(size)}",
            shell=True
        )

        return True