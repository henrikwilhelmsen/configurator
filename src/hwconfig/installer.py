"""Module containing the installer ABC and all installer implementations."""
from __future__ import annotations

import json
import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from hwconfig.config import InstallerConfig

from abc import ABC, abstractmethod
from shutil import copy2, copytree, rmtree

from hwconfig.io import ensure_dir, get_backup_dir
from hwconfig.result import Result


class Installer(ABC):
    """Installer base class."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize the installer with a config."""
        self.config: InstallerConfig = config

    @property
    def backup_dir(self) -> Path:
        """Get path to the backup directory of this installer."""
        return get_backup_dir() / self.config.name

    @abstractmethod
    def install(self: Installer) -> Result:
        """Install the config source files."""
        ...

    @abstractmethod
    def uninstall(self: Installer) -> Result:
        """Uninstall the config files and restore the backup."""
        ...

    @abstractmethod
    def backup(self: Installer) -> Result:
        """Back up the target files to the backup directory."""
        ...


class CopyInstaller(Installer):
    """Installer for config files that only need to be copied to a target location."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize copy installer with a config."""
        super().__init__(config)

    def install(self) -> Result:
        """Install the config files by copying source dir to target."""
        ensure_dir(self.config.target)
        copytree(src=self.config.source, dst=self.config.target, dirs_exist_ok=True)

        return Result.OK

    def uninstall(self) -> Result:
        """Uninstall the config files by deleting them and restoring the backup."""
        rmtree(self.config.target)
        copytree(src=self.backup_dir, dst=self.config.target)

        return Result.OK

    def backup(self) -> Result:
        """Create a backup of the target directory if one does not exist."""
        if self.backup_dir.exists():
            return Result.WARNING

        ensure_dir(self.backup_dir.parent)
        copytree(src=self.config.target, dst=self.backup_dir)

        return Result.OK


class WindowsTerminalInstaller(Installer):
    """Installer for Windows Terminal config."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize the installer with a config."""
        super().__init__(config)

    def install(self) -> Result:
        """Install terminal settings by copying relevant settings from source to destination json."""
        # load source and destination data
        with self.config.source.open() as file:
            source_data = json.load(file)
        with self.config.target.open() as file:
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
        with self.config.target.open("w", encoding="utf-8") as file:
            json.dump(destination_data, file)

        return Result.OK

    def uninstall(self) -> Result:
        """Uninstall the config file by deleting it and restoring the backup."""
        self.config.target.unlink()
        backup_file = self.backup_dir / self.config.target.name
        copy2(src=backup_file, dst=self.config.target)

        return Result.OK

    def backup(self) -> Result:
        """Create a backup of the target settings file if one does not exist."""
        if self.backup_dir.exists():
            return Result.WARNING

        ensure_dir(self.backup_dir)
        copy2(self.config.target, self.backup_dir)

        return Result.OK


INSTALLER_MAP = {
    "copy": CopyInstaller,
    "windows_terminal": WindowsTerminalInstaller,
}


def get_installers(configs: list[InstallerConfig]) -> list[Installer]:
    """Get a list of initialized installers from a list of installer configs.

    Checks config.installer against the INSTALLER_MAP and config.platform against
    platform.system().
    """
    installers: list[Installer] = []

    # Check if each config has an installer that is in the installer map.
    for cfg in configs:
        # If the installer is in the map and on the current platform,
        # initialize it with the config and add to installers list.
        if cfg.installer in INSTALLER_MAP and cfg.platform == platform.system():
            installer = INSTALLER_MAP[cfg.installer](cfg)
            installers.append(installer)

    return installers
