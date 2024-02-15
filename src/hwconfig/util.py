import json
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


def in_linux() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Linux"


def ensure_dir(directory: Path) -> Path:
    if not directory.exists():
        directory.mkdir(parents=True)

    return directory


def check_file_exists(file: Path) -> Result[Path, str]:
    if not file.exists():
        return Err(f"File not found at {file}")

    return Ok(file)


def get_json_data_from_file(file: Path) -> Result[dict[str, str], str]:
    """Get the JSON data from the given file path."""
    if not file.exists():
        return Err(f"File not found at {file}")

    try:
        with file.open(mode="r") as f:
            return Ok(json.load(f))
    except PermissionError as e:
        return Err(str(e))


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


def get_win_terminal_config() -> Path:
    return Path.home().joinpath(
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
        "settings.json",
    )
