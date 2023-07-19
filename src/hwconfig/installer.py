"""Module containing the installer ABC and all installer implementations."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from hwconfig.config import InstallerConfig

from abc import ABC, abstractmethod
from shutil import copytree, rmtree

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
    def __init__(self, config: InstallerConfig) -> None:
        super().__init__(config)

    def install(self) -> Result:
        # TODO
        return NotImplemented

    def uninstall(self) -> Result:
        # TODO
        return NotImplemented

    def backup(self) -> Result:
        # TODO
        return NotImplemented


INSTALLER_MAP = {
    "copy": CopyInstaller,
    "windows_terminal": WindowsTerminalInstaller,
}


def get_installers(configs: list[InstallerConfig]) -> list[Installer]:
    # TODO
    return NotImplemented
