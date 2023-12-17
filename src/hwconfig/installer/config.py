"""Module containing config model classes."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from hwconfig.paths import get_backup_dir

if TYPE_CHECKING:
    from hwconfig.installer.model import InstallerModel


class InstallerConfig:
    """Class representing the config of an installer."""

    def __init__(self, model: InstallerModel) -> None:
        """Initialize the config with a model."""
        self.model: InstallerModel = model
        self._backup_dir: Path | None = None

    @property
    def name(self) -> str:
        """Get the name of the installer."""
        return self.model.name

    @property
    def platform(self) -> str:
        """Get the platform of the installer."""
        return self.model.platform

    @property
    def installer(self) -> str:
        """Get the installer type of the installer.

        See the InstallerModel for valid types.
        """
        return self.model.installer

    @property
    def source(self) -> Path:
        """Get the path to the source directory of the installer."""
        return Path(self.model.source)

    @source.setter
    def source(self, pth: Path) -> None:
        """Set the path to the source of the installer."""
        self.model.source = pth.as_posix()

    @property
    def target(self) -> Path:
        """Get the path to the target of the installer."""
        return Path(self.model.target)

    @target.setter
    def target(self, pth: Path) -> None:
        """Set the path to the target directory of the installer."""
        self.model.target = pth.as_posix()

    @property
    def backup_dir(self) -> Path:
        """Get path to the backup directory of the installer."""
        if not self._backup_dir:
            self._backup_dir = get_backup_dir() / self.name

        return self._backup_dir

    @backup_dir.setter
    def backup_dir(self, pth: Path) -> None:
        """Set the path to the backup directory of the installer."""
        self._backup_dir = pth
