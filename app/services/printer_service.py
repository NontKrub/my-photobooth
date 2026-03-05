import subprocess
from config import PRINTER_NAME


def print_photo(file):

    subprocess.run(
        [
            "lpr",
            "-P",
            PRINTER_NAME,
            str(file),
        ]
    )