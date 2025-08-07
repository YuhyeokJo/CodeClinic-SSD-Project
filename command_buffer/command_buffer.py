import os
from pathlib import Path

MAX_COMMANDS = 5


class CommandBuffer:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "buffer"
        self.output_dir.mkdir(exist_ok=True)

        os.makedirs(self.output_dir, exist_ok=True)
        self._initialize_files()

    def _initialize_files(self):
        # buffer 폴더에 빈 슬롯 초기화
        os.makedirs(self.output_dir, exist_ok=True)

        # 2. 기존 모든 파일 삭제
        for fname in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, fname))

        # 3. 1~5번 슬롯을 empty 파일로 생성
        for i in range(1, MAX_COMMANDS + 1):
            empty_file = os.path.join(self.output_dir, f"{i}_empty")
            open(empty_file, "w").close()

    def _initilize_empty_files(self):
        pass

    def _get_slot_index(self):
        files = sorted(os.listdir(self.output_dir))
        for filename in files:
            if "empty" in filename:
                return int(filename.split("_")[0])
        return None

    def add_command(self, cmd_type, lba, value_or_size):
        slot = self._get_slot_index()
        if slot is None:
            self.flush()
            slot = self._get_slot_index()
        filename = f"{slot}_{cmd_type}_{lba}_{value_or_size}"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write("")  # 내용은 비워두고, 이름만으로 명령 표현
        # 기존 empty 파일 제거
        empty_path = os.path.join(self.output_dir, f"{slot}_empty")
        if os.path.exists(empty_path):
            os.remove(empty_path)
        self.ignore_command_optimization()

    def flush(self):
        self._initialize_files()

    def parse_command(self, filename):
        pass

    def ignore_command_optimization(self):
        pass

    def show_status(self):
        print("=== Buffer 상태 ===")
        for f in sorted(os.listdir(self.output_dir)):
            print(f" - {f}")
