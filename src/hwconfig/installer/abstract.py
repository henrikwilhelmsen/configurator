"""Module containing the Installer base class."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from result import Result

    from hwconfig.installer.config import InstallerConfig
    from hwconfig.settings import Settings

from abc import ABC, abstractmethod


class Installer(ABC):
    """Installer base class."""

    def __init__(self, config: InstallerConfig, settings: Settings) -> None:
        """Initialize the installer with a config."""
        self.config: InstallerConfig = config
        self.settings: Settings = settings

    @abstractmethod
    def backup_dir(self: Installer) -> Path:
        """Get the path to the installer specific backup directory."""
        ...

    @abstractmethod
    def install(self: Installer) -> Result[str, str]:
        """Install the config source files."""
        ...

    @abstractmethod
    def uninstall(self: Installer) -> Result[str, str]:
        """Uninstall the config files and restore the backup."""
        ...

    @abstractmethod
    def backup(self: Installer) -> Result[str, str]:
        """Back up the target files to the backup directory."""
        ...
