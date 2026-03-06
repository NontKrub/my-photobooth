import subprocess
from config import PRINTER_NAME, MOCK_PRINTER


def print_photo(file):
    if MOCK_PRINTER:
        print(f"[mock] Skipping print for {file}")
        return

    subprocess.run(
        [
            "lpr",
            "-P",
            PRINTER_NAME,
            str(file),
        ]
    )