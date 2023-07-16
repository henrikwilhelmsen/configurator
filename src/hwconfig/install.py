from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from hwconfig.io import get_powershell_dir, get_windows_terminal_settings_file


# TODO: Use general copy installer for this
def install_powershell_config(data_dir: Path) -> str:
    """Install PowerShell config by copying the PowerShell config directory.

    Args:
        data_dir: Path to the directory containing the config source data.

    Returns:
        Result of the install.
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


# TODO: Move to WindowsTerminal installer in installer module.
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
