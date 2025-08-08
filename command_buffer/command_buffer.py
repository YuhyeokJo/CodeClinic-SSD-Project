import os
from pathlib import Path

MAX_COMMANDS = 5


class CommandBuffer:
    def __init__(self, on_flush_callback=None):
        self.output_dir = Path(__file__).resolve().parent.parent / "buffer"
        self.output_dir.mkdir(exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.on_flush_callback = on_flush_callback
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

    def _get_slot_index(self):
        files = sorted(os.listdir(self.output_dir))
        for filename in files:
            if "empty" in filename:
                return int(filename.split("_")[0])
        return None

    def add_command(self, cmd_type, lba, value_or_size):
        slot = self._get_slot_index()
        if slot is None:
            # SSD에 flush Callback할 용도
            if self.on_flush_callback:
                self.on_flush_callback()
            else:
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

    def fastread(self, read_lba):
        for fname in reversed(sorted(os.listdir(self.output_dir))):
            if "empty" in fname:
                continue

            parts = fname.split("_")
            cmd_type = parts[1]
            lba = parts[2]
            val_or_size = parts[3]

            if cmd_type == "W":
                if read_lba == lba:
                    return val_or_size

            if cmd_type == "E":
                if read_lba in list(range(int(lba), int(val_or_size))):
                    return "0x00000000"
        return None

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

        # 1. buffer 디렉터리 내 파일 이름에서 명령어 파싱 (empty 파일은 제외)
        for fname in files:
            if "empty" in fname:
                continue
            parsed = self.parse_command(fname)
            if parsed:
                commands.append(parsed)

        # 2. LBA별로 최신 write, 최대 size의 erase 명령 저장
        latest_write = {}
        latest_erase = {}
        for cmd in commands:
            fname, slot, cmd_type, lba, val = cmd
            if cmd_type == "W":
                latest_write[lba] = cmd
            elif cmd_type == "E":
                size = int(val)
                # 동일 LBA에서 size가 더 큰 erase 명령으로 갱신
                if lba not in latest_erase or size > int(latest_erase[lba][4]):
                    latest_erase[lba] = cmd

        # 3. erase 범위에 포함된 write 명령 중 더 늦은 슬롯의 write 명령은 무시
        write_result = []
        for lba, w_cmd in latest_write.items():
            _, write_slot, _, lba, _ = w_cmd
            lba = int(lba)
            erased = False
            for _, erase_slot, _, erase_lba, size in latest_erase.values():
                erase_lba = int(erase_lba)
                size = int(size)
                # erase 범위 내 write이면서 erase 명령이 더 늦게 발생했으면 무시
                if erase_lba <= lba < erase_lba + size and erase_slot > write_slot:
                    erased = True
                    break
            if not erased:
                write_result.append(w_cmd)

        # 4. erase 명령을 LBA 범위 기준으로 병합 (인접 구간 병합)
        intervals = []
        for fname, slot, cmd, lba, size in latest_erase.values():
            lba = int(lba)
            size = int(size)
            start = lba
            end = lba + size - 1
            intervals.append((start, end, slot))

        intervals.sort(key=lambda x: x[0])

        erased_merged = []
        for start, end, slot in intervals:
            if not erased_merged:
                erased_merged.append((start, end, slot))
            else:
                last_start, last_end, last_slot = erased_merged[-1]
                if start <= last_end + 1:
                    new_start = min(start, last_start)
                    new_end = max(end, last_end)
                    new_slot = min(slot, last_slot)
                    erased_merged[-1] = (new_start, new_end, new_slot)
                else:
                    erased_merged.append((start, end, slot))

        # 5. write LBA를 제외하지 않은 경우와 제외한 경우 각각의 erase 결과 생성
        write_lbas = {int(cmd[3]) for cmd in write_result}

        # (1) write LBA를 제외하지 않고 최대 10개씩 나눠 저장
        erased_original_result = []
        for start, end, slot in erased_merged:
            curr = start
            while curr <= end:
                next_end = min(curr + 9, end)  # 최대 10칸
                size = next_end - curr + 1
                fname = f"{slot}_E_{curr}_{size}"
                erased_original_result.append((fname, slot, "E", curr, str(size)))
                curr = next_end + 1

        # (2) write LBA를 제외하고, write가 있는 LBA를 건너뛰어 최대 10칸씩 분할
        erased_exclude_write_result = []
        for start, end, slot in erased_merged:
            erase_ranges = []
            curr = start
            while curr <= end:
                if curr in write_lbas:
                    curr += 1
                    continue
                erase_start = curr
                while curr <= end and curr not in write_lbas:
                    curr += 1
                erase_end = curr - 1
                if erase_start <= erase_end:
                    erase_ranges.append((erase_start, erase_end))
            for er_start, er_end in erase_ranges:
                curr = er_start
                while curr <= er_end:
                    next_end = min(curr + 9, er_end)
                    size = next_end - curr + 1
                    fname = f"{slot}_E_{curr}_{size}"
                    erased_exclude_write_result.append((fname, slot, "E", curr, str(size)))
                    curr = next_end + 1

        # 6. write 포함 명령 개수를 비교하여, 더 적은 개수인 erase 결과 선택
        count_original = len(erased_original_result) + len(write_result)
        count_exclude_write = len(erased_exclude_write_result) + len(write_result)

        if count_exclude_write <= count_original:
            final_erase_result = erased_exclude_write_result
        else:
            final_erase_result = erased_original_result

        # 7. 최종 명령 조합: erase 명령 먼저, write 명령은 뒤에 배치
        final_cmds = final_erase_result + write_result
        final_cmds.sort(key=lambda x: (x[1], x[2]))  # slot, cmd_type 순

        # 8. 기존 명령 파일 삭제
        for fname in files:
            if "empty" not in fname:
                os.remove(os.path.join(self.output_dir, fname))

        # 9. 최종 명령을 파일로 저장, 1번 슬롯부터 순서대로
        for idx, (_, _, cmd, lba, val) in enumerate(final_cmds, start=1):
            new_fname = f"{idx}_{cmd}_{lba}_{val}"
            with open(os.path.join(self.output_dir, new_fname), "w") as f:
                f.write("")

        # 10. 남은 슬롯은 empty 파일로 채움
        for i in range(len(final_cmds) + 1, 6):
            open(os.path.join(self.output_dir, f"{i}_empty"), "w").close()

    def show_status(self):
        for f in sorted(os.listdir(self.output_dir)):
            print(f" - {f}")

    def get_commands(self):
        commands = []
        for fname in sorted(os.listdir(self.output_dir)):
            if "empty" in fname:
                continue
            parts = fname.split("_")
            if len(parts) != 4:
                continue
            slot = int(parts[0])
            cmd_type = parts[1]
            lba = parts[2]
            val_or_size = parts[3]
            commands.append((slot, cmd_type, lba, val_or_size))
        return commands
