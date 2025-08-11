import os
from pathlib import Path

MAX_COMMANDS = 5


class CommandBuffer:
    def __init__(self, on_flush_callback=None):
        self.output_dir = Path(__file__).resolve().parent.parent / "buffer"
        self.output_dir.mkdir(exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.on_flush_callback = on_flush_callback

    def initialize_buffer(self):
        # buffer 폴더에 빈 슬롯 초기화
        os.makedirs(self.output_dir, exist_ok=True)

        # 2. 기존 모든 파일 삭제
        for filename in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, filename))

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
        self.optimize_commands()

    def fastread(self, read_lba):
        for fname in reversed(sorted(os.listdir(self.output_dir))):
            if "empty" in fname:
                continue

            parts = fname.split("_")
            cmd_type = parts[1]
            lba = parts[2]
            val_or_size = parts[3]

            if cmd_type == "W":
                if int(read_lba) == int(lba):
                    return val_or_size

            if cmd_type == "E":
                if int(lba) <= int(read_lba) < int(lba) + int(val_or_size):
                    return "0x00000000"
        return None

    def flush(self):
        self.initialize_buffer()

    def parse_command(self, filename):
        parts = filename.split("_")
        if len(parts) != 4:
            return None

        slot = int(parts[0])
        cmd_type = parts[1]
        lba = int(parts[2])
        if cmd_type == "E":
            val_or_size = int(parts[3])
        else:
            val_or_size = parts[3]

        return (filename, slot, cmd_type, lba, val_or_size)

    def _get_active_commands(self):
        files = os.listdir(self.output_dir)
        commands = []

        for filename in files:
            if "empty" in filename:
                continue
            parsed = self.parse_command(filename)
            if parsed:
                commands.append(parsed)
        return commands

    def _select_effective_commands(self, commands):
        latest_write = {}
        latest_erase = {}
        for cmd in commands:
            _, slot, cmd_type, lba, val = cmd
            if cmd_type == "W":
                if commands[-1][2] == 'E':
                    _, _, _, e_lba, e_size = commands[-1]
                    if e_lba <= lba < e_lba + e_size:
                        continue
                latest_write[lba] = cmd
            elif cmd_type == "E":
                size = val
                if lba not in latest_erase or size > int(latest_erase[lba][4]):
                    latest_erase[lba] = cmd

        return list(latest_write.values()), list(latest_erase.values())

    def _merge_erases(self, erase_cmds):
        intervals = sorted([(lba, lba + size - 1, slot) for _, slot, _, lba, size in erase_cmds])

        if not intervals:
            return []

        merged_intervals = [intervals[0]]
        for start, end, slot in intervals[1:]:
            last_start, last_end, last_slot = merged_intervals[-1]

            if start <= last_end + 1:
                new_start = min(start, last_start)
                new_end = max(end, last_end)
                new_slot = min(slot, last_slot)

                merged_intervals[-1] = (new_start, new_end, new_slot)
            else:
                merged_intervals.append((start, end, slot))

        merged_erases = []
        for start, end, slot in merged_intervals:
            size = end - start + 1
            merged_erases.append((f"{slot}_E_{start}_{size}", slot, "E", start, size))

        return merged_erases

    def _split_erases(self, merged_erases, write_lbas, exclude_writes=False):
        final_erases = []
        for _, slot, cmd_type, start, size in merged_erases:
            end = start + size - 1
            current = start

            while current <= end:
                if exclude_writes and current in write_lbas:
                    current += 1
                    continue
                chunk_start = current
                chunk_end = min(chunk_start + 9, end)

                if exclude_writes:
                    while chunk_end in write_lbas and chunk_end >= chunk_start:
                        chunk_end -= 1

                if chunk_start > chunk_end:
                    current = chunk_start + 1
                    continue

                chunk_size = chunk_end - chunk_start + 1
                filename = f"{slot}_{cmd_type}_{chunk_start}_{chunk_size}"

                final_erases.append(((filename, slot, cmd_type, chunk_start, chunk_size)))
                current = chunk_end + 1
        return final_erases

    def _write_final_commands_to_buffer(self, final_cmds):
        for file in self.output_dir.iterdir():
            if "empty" not in file.name:
                file.unlink()

        for idx, (_, _, cmd, lba, val) in enumerate(final_cmds, 1):
            new_filename = f"{idx}_{cmd}_{lba}_{val}"
            with open(os.path.join(self.output_dir, new_filename), "w") as f:
                f.write("")

        for i in range(len(final_cmds) + 1, 6):
            open(os.path.join(self.output_dir, f"{i}_empty"), "w").close()

    def optimize_commands(self):
        # 1. buffer 디렉터리 내 파일 이름에서 명령어 파싱 (empty 파일은 제외)
        commands = self._get_active_commands()

        # 2. LBA별로 최신 write, 최대 size의 erase 명령 저장, 새로운 erase command 범위에 write가 있다면 무시
        final_writes, erase_cmds = self._select_effective_commands(commands)

        # 3. erase 명령을 LBA 범위 기준으로 병합 (인접 구간 병합)
        merged_erases = self._merge_erases(erase_cmds)

        # 4. write LBA를 제외하지 않은 경우와 제외한 경우 각각의 erase 결과 생성
        write_lbas = {lba for _, _, _, lba, _ in final_writes}

        final_erases_with_writes = self._split_erases(merged_erases, write_lbas, exclude_writes=False)
        count_with_writes = len(final_erases_with_writes) + len(final_writes)

        final_erases_without_writes = self._split_erases(merged_erases, write_lbas, exclude_writes=True)
        count_without_writes = len(final_erases_without_writes) + len(final_writes)

        # 5. write 포함 명령 개수를 비교하여, 더 적은 개수인 erase 결과 선택
        final_erases = []
        if count_without_writes < count_with_writes:
            final_erases = final_erases_without_writes
        else:
            final_erases = final_erases_with_writes

        # 6. 최종 명령 조합
        final_cmds = sorted(final_erases + final_writes, key=lambda x: (x[1], x[2], x[3]))  # slot, cmd_type, lba

        # 7. 버퍼 디렉토리에 다시 작성
        self._write_final_commands_to_buffer(final_cmds)

    def show_status(self):
        files = []
        for f in sorted(os.listdir(self.output_dir)):
            files.append(f)
        return files

    def get_commands(self):
        commands = []
        for filename in sorted(os.listdir(self.output_dir)):
            if "empty" in filename:
                continue
            parts = filename.split("_")
            if len(parts) != 4:
                continue
            slot = int(parts[0])
            cmd_type = parts[1]
            lba = parts[2]
            val_or_size = parts[3]
            commands.append((slot, cmd_type, lba, val_or_size))
        return commands
