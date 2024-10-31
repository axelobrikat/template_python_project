from pathlib import Path
import logging


SEPARATOR: str = "========================================"
"""returns a line that acts as a visual separator"""


def log_exec_start_msg(log_file_path: Path):
    """log a debug msg for program execution start

    Args:
        log_file_path (Path): path to log file
    """
    logging.debug((
        f"Program execution starts.\n"
        f"Logging and Input Arguments configured successfully.\n"
        f"Log rotation of log files '{log_file_path}.<x>' performed succesfully.\n"
        f"{SEPARATOR}\n"
        f"{SEPARATOR}\n\n"
    ))
