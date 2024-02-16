from pathlib import Path
from subprocess import CalledProcessError, check_output

from result import Err, Ok, Result

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.copy import CopyInstaller
from hwconfig.installer.protocol import Installer
from hwconfig.installer.terminal import TerminalInstaller
from hwconfig.settings import get_settings
from hwconfig.util import in_linux, in_windows


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


def get_win_terminal_config_dir() -> Path:
    """Get the path to the Windows Terminal settings.json file."""
    return Path.home().joinpath(
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
    )


def get_flow_config() -> Result[Path, str]:
    """Get the path to the Flow Launcher Settings.json file. (When installed with Scoop).

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


def powershell_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "powershell"

    match get_powershell_dir():
        case Ok(v):
            target = v
        case Err(e):
            return Err(f"Could not get powershell dir: {e}")

    installer_config = InstallerConfig(name="powershell", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def terminal_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "terminal"
    target = get_win_terminal_config_dir()
    installer_config = InstallerConfig(name="terminal", source=source, target=target)

    return Ok(TerminalInstaller(config=installer_config))


def flow_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "flow"

    match get_flow_config():
        case Ok(v):
            target = v
        case Err(e):
            return Err(e)

    installer_config = InstallerConfig(name="flow", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def fish_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "fish"
    target = Path.home() / ".config" / "fish"

    installer_config = InstallerConfig(name="fish", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def hyper_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "hyper"
    target = Path.home()

    installer_config = InstallerConfig(name="hyper", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def windows_installers() -> Result[list[Installer], str]:
    installers: list[Installer] = []

    for r in (powershell_installer(), terminal_installer(), flow_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def linux_installers() -> Result[list[Installer], str]:
    installers: list[Installer] = []

    for r in (fish_installer(), hyper_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def installers() -> Result[list[Installer], str]:
    if in_windows():
        return windows_installers()
    if in_linux():
        return linux_installers()

    return Err("Unsupported platform.")
