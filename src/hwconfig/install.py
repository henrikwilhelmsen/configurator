import json
import platform
import os
from typing import Generator, List, Callable
from pathlib import Path
from shutil import copytree
from subprocess import check_call

from hwconfig.lib import (
    get_powershell_dir,
    ensure_dir,
    in_wsl,
    get_windows_terminal_settings_file,
)


def get_config_data_repo() -> str:
    source_env = os.getenv("HWCONFIG_DATA_SOURCE")
    if source_env:
        return source_env

    return "https://github.com/henrikwilhelmsen/hw-config-data.git"


HWCONFIG_DIR = Path.home() / ".hwconfig"
CONFIG_DATA_REPO = get_config_data_repo()
CONFIG_DATA_NAME = CONFIG_DATA_REPO.rsplit("/", maxsplit=-1)[-1].split(".")[0]
CONFIG_DATA_DIR = HWCONFIG_DIR / CONFIG_DATA_NAME

Installer = Callable[[], str]


def get_config_data() -> None:
    if not HWCONFIG_DIR.exists():
        HWCONFIG_DIR.mkdir(parents=True)

    args = ["git", "clone", CONFIG_DATA_REPO]
    check_call(args=args, cwd=HWCONFIG_DIR)


def update_config_data() -> None:

    if not CONFIG_DATA_DIR.exists():
        get_config_data()

    args = ["git", "pull"]
    check_call(args=args, cwd=CONFIG_DATA_DIR)


def install_powershell_config() -> str:
    """Install PowerShell config by copying the PowerShell config directory.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = HWCONFIG_DIR / "powershell"
    target_dir = get_powershell_dir()

    if not target_dir:
        return "Unable to locate powershell config dir, skipping install."

    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Powershell config installed ({target_dir})"


def copy_terminal_settings(source_file: Path, destination_file: Path) -> None:
    """
    Copy the default profile settings, application settings and schemes from source json
    to the destination json file.

    Windows terminal has additional settings like WSL profiles that are difficult to
    share between systems and that we would not want to override by just replacing the
    file, like with the other config files.
    """
    # load source and destination data
    with open(source_file, encoding="utf-8") as file:
        source_data = json.load(file)
    with open(destination_file, encoding="utf-8") as file:
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
    with open(destination_file, "w", encoding="utf-8") as file:
        json.dump(destination_data, file)


def install_windows_terminal_config() -> str:
    """Install Windows Terminal config.

    Does not overwrite the entire file, but inserts overrides on theme and appearance
    in the user config, so local path settings etc are not lost.

    Returns:
        A string saying the config was installed and to which file.
    """
    source_config = CONFIG_DATA_DIR / "terminal" / "settings.json"
    target_config = get_windows_terminal_settings_file()

    if not target_config:
        return "Unable to locate terminal setting.json, skipping"

    copy_terminal_settings(source_file=source_config, destination_file=target_config)
    return f"windows terminal config installed ({target_config})"


def install_fish_config() -> str:
    """Install Fish config by copying the contents of the Fish config directory.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = CONFIG_DATA_DIR / "fish"
    target_dir = ensure_dir(Path.home().joinpath(".config/fish"))
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Fish config installed ({target_dir})"


def install_alacritty_config() -> str:
    """
    Install Alacritty config by copying the contents of the Alacritty config directory.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = CONFIG_DATA_DIR / "alacritty"
    target_dir = ensure_dir(Path.home().joinpath(".config/alacritty"))
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Alacritty config installed ({target_dir})"


def install_hyper_config() -> str:
    """Install Hyper config by copying the contents of the Hyper config directory.

    Returns:
        A string saying the config was installed and to which directory.
    """
    source_dir = CONFIG_DATA_DIR / "hyper"
    target_dir = ensure_dir(Path.home())
    copytree(src=source_dir, dst=target_dir, dirs_exist_ok=True)
    return f"Hyper config installed ({target_dir})"


def get_linux_installers() -> List[Installer]:
    """Get Linux installers.

    Returns:
        A list of all the Linux installers.
    """
    installers = [install_fish_config]

    if not in_wsl():
        installers.append(install_hyper_config)

    return installers


def get_windows_installers() -> List[Installer]:
    """Get Windows installers.

    Returns:
        A list of all the Windows config installers.
    """
    return [install_powershell_config, install_windows_terminal_config]


def get_installers() -> Generator[Installer, None, None]:
    """Gets the installers for the current platform. (Windows or Linux)

    Raises:
        NotImplementedError: If the current platform is not supported.

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
        raise NotImplementedError(f"No config installers found for {platform.system()}")
