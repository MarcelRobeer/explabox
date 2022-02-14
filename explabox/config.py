"""Configuration for default paths and variables."""

from pathlib import Path

# Paths
CWD: str = Path().cwd()
OUTPUT_DIR: str = f"{CWD}/output"
