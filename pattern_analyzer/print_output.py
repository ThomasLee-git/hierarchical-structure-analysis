from multiprocessing.spawn import import_main_path
from pathlib import Path

if __name__ == "__main__":
    input_root = Path("/tmp/thomas_ramdisk/hooktheory_analyzed_patterns")
    for d in input_root.iterdir():
        if d.is_dir():
            log_path = d.joinpath("phrases_log.txt")
            with open(log_path, mode="r") as rf:
                lines = rf.read().splitlines()
            print(f"{' '.join(lines)}")
