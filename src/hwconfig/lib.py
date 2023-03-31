from pathlib import Path
import platform
from subprocess import CalledProcessError, check_output
from typing import Union


def in_wsl() -> bool:
    """Check if we are running in a WSL instance.

    Returns:
        True if running in a WSL instance, False if not.
    """
    return "microsoft-standard" in platform.uname().release


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


def get_powershell_dir() -> Union[Path, None]:
    """Get the PowerShell user directory located in <user_paths>/Documents/PowerShell

    Returns:
        The path to the PowerShell directory as a Path object if it exists, else None.
    """
    try:
        documents_dir = check_output(
            args=["powershell.exe", "[Environment]::GetFolderPath('MyDocuments')"],
            encoding="utf-8",
            shell=True,
        ).splitlines()[0]

    except CalledProcessError as err:
        print(f"Unable to locate documents folder ({err})")
        return None

    powershell_dir = Path(documents_dir) / "PowerShell"

    if powershell_dir.exists():
        return powershell_dir

    print(f"No PowerShell directory in documents folder ({documents_dir}")
    return None


def get_windows_terminal_settings_file() -> Union[Path, None]:
    """Get the path to the Windows Terminal settings.json file, if it exists

    Returns:
        The path to the settings file if it exists, None if not.
    """
    terminal_settings_file = Path.home().joinpath(
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
        "settings.json",
    )

    if terminal_settings_file.exists():
        return terminal_settings_file

    return None
