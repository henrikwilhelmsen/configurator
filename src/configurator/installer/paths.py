from pathlib import Path
from subprocess import CalledProcessError, check_output

from result import Err, Ok, Result


def get_powershell_config_dir() -> Result[Path, str]:
    """Get the PowerShell user directory located in <user_paths>/Documents/PowerShell."""
    try:
        documents_dir = check_output(
            args=["powershell.exe", "[Environment]::GetFolderPath('MyDocuments')"],
            encoding="utf-8",
            shell=True,
        ).splitlines()[0]

    except CalledProcessError as e:
        return Err(f"Failed to retrieve PowerShell user directory: {e.output}")

    powershell_dir = Path(documents_dir) / "PowerShell"
    if not powershell_dir.exists():
        return Err("PowerShell user directory not found.")

    return Ok(powershell_dir)


def get_win_terminal_config_dir() -> Result[Path, str]:
    """Get the path to the Windows Terminal config directory."""
    config_dir = Path.home().joinpath(
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
    )

    if not config_dir.exists():
        return Err("Windows Terminal config directory not found.")

    return Ok(config_dir)


def get_flow_config_dir() -> Result[Path, str]:
    """Get the path to the Flow Launcher config directory. (When installed with Scoop).

    C:/Users/<username>/scoop/apps/flow-launcher/current/app-<version>/UserData/Settings/
    """
    flow_dir = Path.home() / "scoop" / "apps" / "flow-launcher" / "current"
    config_dir: Path | None = None

    for p in flow_dir.glob("*"):
        if p.is_dir() and p.name.startswith("app-"):
            config_dir = p / "UserData" / "Settings"

    if config_dir and config_dir.exists():
        return Ok(config_dir)

    return Err("Flow config not found.")
