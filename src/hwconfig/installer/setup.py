from pathlib import Path

from result import Err, Ok, Result

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.copy import CopyInstaller
from hwconfig.installer.protocol import Installer
from hwconfig.installer.terminal import TerminalInstaller
from hwconfig.settings import get_settings
from hwconfig.util import get_powershell_dir, get_win_terminal_config, in_linux, in_windows


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
    source = settings.data_repo_dir / "terminal" / "settings.json"
    target = get_win_terminal_config()
    installer_config = InstallerConfig(name="terminal", source=source, target=target)

    return Ok(TerminalInstaller(config=installer_config))


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

    for r in (powershell_installer(), terminal_installer()):
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
