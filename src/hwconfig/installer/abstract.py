"""Module containing the Installer base class."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from hwconfig.installer.config import InstallerConfig
    from hwconfig.result import Result

from abc import ABC, abstractmethod

from hwconfig.paths import get_backup_dir


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
