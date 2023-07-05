from __future__ import annotations

import json
import platform
from collections.abc import Callable, Generator
from pathlib import Path
from shutil import copytree

from hwconfig.constants import DATA_DIR_NAME, get_config_data_url, get_hwconfig_home_dir
from hwconfig.lib import (
    clone_repo,
    ensure_dir,
    get_powershell_dir,
    get_windows_terminal_settings_file,
    in_wsl,
    update_repo,
)

Installer = Callable[..., str]

# TODO: Installer error reporting and checks


def get_sync_config_data_dir() -> Path:
    """Sync the config data directory and return the local path to it.

    Returns:
        The path to the config data directory.
    """
    data_url = get_config_data_url()

    hwconfig_home_dir = get_hwconfig_home_dir()
    hwconfig_data_dir = hwconfig_home_dir / DATA_DIR_NAME

    if not hwconfig_home_dir.exists():
        hwconfig_home_dir.mkdir(parents=True)

    if not hwconfig_data_dir.exists():
        clone_repo(
            src_url=data_url, dst_dir=hwconfig_home_dir, repo_dir_name=DATA_DIR_NAME,
        )
    else:
        update_repo(repo_dir=hwconfig_data_dir)

    return hwconfig_data_dir


def install_powershell_config(data_dir: Path) -> str:
    """Install PowerShell config by copying the PowerShell config directory.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = data_dir / "powershell"
    target_dir = get_powershell_dir()

    if not target_dir:
        return "Unable to locate powershell config dir, skipping install."

    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Powershell config installed ({target_dir})"


def copy_terminal_settings(source_file: Path, destination_file: Path) -> None:
    """Copy the default profile settings, application settings and schemes.

    Windows terminal has additional settings like WSL profiles that are difficult to
    share between systems and that we would not want to override by just replacing the
    file, like with the other config files.

    Args:
        source_file: The file containing the settings to copy.
        destination_file: The file to copy the settings to.
    """
    # load source and destination data
    with source_file.open() as file:
        source_data = json.load(file)
    with destination_file.open() as file:
        destination_data = json.load(file)

    # update default settings
    destination_data["profiles"]["defaults"] = source_data["profiles"]["defaults"]

    # update schemes, only add/override schemes found in source data
    source_schemes: list[dict] = source_data["schemes"]
    destination_schemes: list[dict] = destination_data["schemes"]
    source_scheme_names = [x["name"] for x in source_schemes]

    # remove any destination scheme that exists in source schemes
    for n, scheme in enumerate(destination_schemes):
        if scheme["name"] in source_scheme_names:
            destination_schemes.pop(n)

    # add source schemes to destination schemes
    destination_schemes.extend(source_schemes)
    destination_data["schemes"] = destination_schemes

    # update application settings, not nested in destination only source
    source_application_data: dict = source_data["application"]

    for key, value in source_application_data.items():
        destination_data[key] = value

    # write to destination file
    with destination_file.open("w", encoding="utf-8") as file:
        json.dump(destination_data, file)


def install_windows_terminal_config(data_dir: Path) -> str:
    """Install Windows Terminal config.

    Does not overwrite the entire file, but inserts overrides on theme and appearance
    in the user config, so local path settings etc are not lost.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        Result of the installation.
    """
    source_config = data_dir / "terminal" / "settings.json"
    target_config = get_windows_terminal_settings_file()

    if not target_config:
        return "Unable to locate terminal setting.json, skipping"

    copy_terminal_settings(source_file=source_config, destination_file=target_config)
    return f"windows terminal config installed ({target_config})"


# TODO: Generalized implementation, copying code for all the basic installers atm.
def install_fish_config(data_dir: Path) -> str:
    """Install Fish config by copying the contents of the Fish config directory.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = data_dir / "fish"
    target_dir = ensure_dir(Path.home().joinpath(".config/fish"))
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Fish config installed ({target_dir})"


def install_alacritty_config(data_dir: Path) -> str:
    """Install Alacritty config by copying.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        The result of the installation process.
    """
    source_dir = data_dir / "alacritty"
    target_dir = ensure_dir(Path.home().joinpath(".config/alacritty"))
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Alacritty config installed ({target_dir})"


def install_hyper_config(data_dir: Path) -> str:
    """Install Hyper config by copying.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = data_dir / "hyper"
    target_dir = ensure_dir(Path.home())
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Hyper config installed ({target_dir})"


def get_linux_installers() -> list[Installer]:
    """Get Linux installers.

    Returns:
        A list of all the Linux installers.
    """
    installers = [install_fish_config]

    if not in_wsl():
        installers.append(install_hyper_config)

    return installers


def get_windows_installers() -> list[Installer]:
    """Get Windows installers.

    Returns:
        A list of all the Windows config installers.
    """
    return [install_powershell_config, install_windows_terminal_config]


def get_installers() -> Generator[Installer, None, None]:
    """Gets the installers for the current platform (Windows or Linux).

    Raises:
        NotImplementedError: If current platform does not have installers implemented.

    Yields:
        Every config installer for the current platform.
    """
    if platform.system() == "Linux":
        for installer in get_linux_installers():
            yield installer
    elif platform.system() == "Windows":
        for installer in get_windows_installers():
            yield installer
    else:
        raise NotImplementedError
