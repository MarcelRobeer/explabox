"""Utility functions for input/output behavior."""

from pathlib import Path

from ..config import OUTPUT_DIR


def create_output_dir(path: str = OUTPUT_DIR):
    """Create the directory to write results to.

    Args:
        path (str, optional): Path of the directory where to write any results to. Defaults to OUTPUT_DIR.
    """
    path = str(path)

    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass
    else:
        print(f"Output folder located at {str(OUTPUT_DIR)}")
