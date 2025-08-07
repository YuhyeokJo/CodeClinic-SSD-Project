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
        parts = filename.split("_")
        if len(parts) != 4:
            return None
        slot = int(parts[0])
        cmd_type = parts[1]
        lba = int(parts[2])
        val_or_size = parts[3]
        return (filename, slot, cmd_type, lba, val_or_size)

    def ignore_command_optimization(self):
        files = os.listdir(self.output_dir)
        commands = []

        # 1. 파일 이름에서 명령어 파싱
        for fname in files:
            if "empty" in fname:
                continue
            parsed = self.parse_command(fname)
            if parsed:
                commands.append(parsed)

        # 2. 같은 lba (가장 마지막 것만 남김)
        latest_write = {}
        latest_erase = {}
        for cmd in commands:
            fname, slot, cmd_type, lba, val = cmd
            if cmd_type == "W":
                latest_write[lba] = cmd
            elif cmd_type == "E":
                size = int(val)
                if lba not in latest_erase or size > int(latest_erase[lba][4]):
                    latest_erase[lba] = cmd

        result = []
        # 3. erase 변위에 write가 선행되어 있으면 제거
        for lba, w_cmd in latest_write.items():
            _, write_slot, _, lba, _ = w_cmd
            lba = int(lba)
            erased = False
            for _, erase_slot, _, erase_lba, size in latest_erase.values():
                erase_lba = int(erase_lba)
                size = int(size)
                if erase_lba <= lba < erase_lba + size and erase_slot > write_slot:
                    erased = True
                    break
            if not erased:
                result.append(w_cmd)

        erase_merged = []
        for cmd in latest_erase.values():
            _, slot, command, lba, size = cmd
            lba = int(lba)
            size = int(size)
            start1 = lba
            end1 = lba + size - 1

            merged_flag = False

            for i in range(len(erase_merged)):
                _, _, _, mlba, msize = erase_merged[i]
                mlba = int(mlba)
                msize = int(msize)
                start2 = mlba
                end2 = mlba + msize - 1

                # 겹치거나 인접한 경우 병합
                if max(start1, start2) <= min(end1, end2) + 1:
                    new_start = min(start1, start2)
                    new_end = max(end1, end2)
                    new_size = new_end - new_start + 1

                    if new_size <= 10:
                        # 병합 → 기존 항목 교체
                        new_fname = f"{slot}_E_{new_start}_{new_size}"
                        erase_merged[i] = (new_fname, slot, "E", new_start, str(new_size))
                        merged_flag = True
                        break

            if not merged_flag:
                erase_merged.append(cmd)

        final_cmds = result + erase_merged

        for fname in files:
            if "empty" not in fname:
                os.remove(os.path.join(self.output_dir, fname))

        # 재저장: 1부터 차례대로
        for idx, (_, _, cmd, lba, val) in enumerate(final_cmds, start=1):
            new_fname = f"{idx}_{cmd}_{lba}_{val}"
            with open(os.path.join(self.output_dir, new_fname), "w") as f:
                f.write("")

            # 남는 슬롯은 empty로 채우기
        for i in range(len(final_cmds) + 1, 6):
            open(os.path.join(self.output_dir, f"{i}_empty"), "w").close()

    def show_status(self):
        print("=== Buffer 상태 ===")
        for f in sorted(os.listdir(self.output_dir)):
            print(f" - {f}")
