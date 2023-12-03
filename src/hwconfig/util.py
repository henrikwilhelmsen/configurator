"""Platform related utility functions."""
import platform
from pathlib import Path
from subprocess import CalledProcessError, check_output

from result import Err, Ok, Result


def in_wsl() -> bool:
    """Check if we are running in a WSL instance."""
    return "microsoft-standard" in platform.uname().release


def in_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"


def ensure_dir(directory: Path) -> Path:
    """Create the given directory if it does not already exist.

    Args:
        directory: The directory to create.

    Returns:
        The path of the created directory.
    """
    if not directory.exists():
        directory.mkdir(parents=True)

    return directory


def get_powershell_dir() -> Result[Path, str]:
    """Get the PowerShell user directory located in <user_paths>/Documents/PowerShell."""
    try:
        documents_dir = check_output(
            args=["powershell.exe", "[Environment]::GetFolderPath('MyDocuments')"],
            encoding="utf-8",
            shell=True,
        ).splitlines()[0]

    except CalledProcessError as e:
        return Err(e.output)

    powershell_dir = Path(documents_dir) / "PowerShell"

    if powershell_dir.exists():
        return Ok(powershell_dir)

    return Err("Powershell directory does not exist.")
