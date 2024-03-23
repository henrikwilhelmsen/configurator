"""Installer setup functions."""
from pathlib import Path

from result import Err, Ok, Result

from configurator.installer.config import InstallerConfig
from configurator.installer.copy import CopyInstaller
from configurator.installer.paths import (
    get_flow_config_dir,
    get_powershell_config_dir,
    get_win_terminal_config_dir,
)
from configurator.installer.protocol import Installer
from configurator.installer.terminal import TerminalInstaller
from configurator.settings import get_settings
from configurator.util import in_linux, in_windows


def powershell_installer() -> Result[Installer, str]:
    """Set up the installer for the PowerShell config.

    Returns:
        A result containing the installer or an error message.
    """
    settings = get_settings()
    source = settings.data_repo_dir / "powershell"

    match get_powershell_config_dir():
        case Ok(v):
            target = v
        case Err(e):
            return Err(f"Could not get powershell dir: {e}")

    installer_config = InstallerConfig(name="powershell", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def terminal_installer() -> Result[Installer, str]:
    """Set up the installer for the Windows Terminal config.

    Returns:
        A result containing the installer or an error message.
    """
    settings = get_settings()
    source = settings.data_repo_dir / "terminal"

    match get_win_terminal_config_dir():
        case Ok(v):
            target = v
        case Err(e):
            return Err(f"Could not get terminal dir: {e}")

    installer_config = InstallerConfig(name="terminal", source=source, target=target)
    return Ok(TerminalInstaller(config=installer_config))


def flow_installer() -> Result[Installer, str]:
    """Set up the installer for the Flow config.

    Returns:
        A result containing the installer or an error message.
    """
    settings = get_settings()
    source = settings.data_repo_dir / "flow"

    match get_flow_config_dir():
        case Ok(v):
            target = v
        case Err(e):
            return Err(e)

    installer_config = InstallerConfig(name="flow", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def fish_installer() -> Result[Installer, str]:
    """Set up the installer for the Fish config.

    Returns:
        A result containing the installer or an error message.
    """
    settings = get_settings()
    source = settings.data_repo_dir / "fish"
    target = Path.home() / ".config" / "fish"

    installer_config = InstallerConfig(name="fish", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def hyper_installer() -> Result[Installer, str]:
    """Set up the installer for the Hyper config.

    Returns:
        A result containing the installer or an error message.
    """
    settings = get_settings()
    source = settings.data_repo_dir / "hyper"
    target = Path.home()

    installer_config = InstallerConfig(name="hyper", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def windows_installers() -> Result[list[Installer], str]:
    """Set up the installers for the Windows configs.

    Returns:
        A result containing the installers or an error message.
    """
    installers: list[Installer] = []

    for r in (powershell_installer(), terminal_installer(), flow_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def linux_installers() -> Result[list[Installer], str]:
    """Set up the installers for the Linux configs.

    Returns:
        A result containing the installers or an error message.
    """
    installers: list[Installer] = []

    for r in (fish_installer(), hyper_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def get_installers() -> Result[list[Installer], str]:
    """Set up the installers for the current platform.

    Returns:
        A result containing the installers or an error message.
    """
    if in_windows():
        return windows_installers()
    if in_linux():
        return linux_installers()

    return Err("Unsupported platform.")
