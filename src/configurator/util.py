"""Utility functions."""
import json
import platform
from pathlib import Path

from result import Err, Ok, Result


def in_wsl() -> bool:
    """Check if we are running in a WSL instance."""
    return "microsoft-standard" in platform.uname().release


def in_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"


def in_linux() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Linux"


def ensure_dir(directory: Path) -> Path:
    """Ensure the given directory exists.

    Args:
        directory: The directory to ensure exists.

    Returns:
        Path to the directory.
    """
    if not directory.exists():
        directory.mkdir(parents=True)

    return directory


def check_file_exists(file: Path) -> Result[Path, str]:
    """Check if a file exists.

    Args:
        file: The file to check.

    Returns:
        A result containing the path to the file, or an error message.
    """
    if not file.exists():
        return Err(f"File not found at {file}")

    return Ok(file)


def get_json_data_from_file(file: Path) -> Result[dict[str, str], str]:
    """Get JSON data from a file.

    Args:
        file: The file to read.

    Returns:
        A result containing the JSON data from the file, or an error message.
    """
    if not file.exists():
        return Err(f"File not found at {file}")

    try:
        with file.open(mode="r") as f:
            return Ok(json.load(f))
    except PermissionError as e:
        return Err(str(e))
