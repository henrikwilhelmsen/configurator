"""Module containing config model classes."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hwconfig.models import InstallerModel


class InstallerConfig:
    def __init__(self, model: InstallerModel) -> None:
        self.model: InstallerModel = model

    @property
    def name(self) -> str:
        return self.model.name

    @name.setter
    def name(self, name: str) -> None:
        self.model.name = name

    @property
    def platform(self) -> str:
        return self.model.platform

    @platform.setter
    def platform(self, platform: str) -> None:
        self.model.platform = platform

    @property
    def installer(self) -> str:
        return self.model.installer

    @installer.setter
    def installer(self, installer: str) -> None:
        self.model.installer = installer

    @property
    def source(self) -> Path:
        return Path(self.model.source)

    @source.setter
    def source(self, source: Path) -> None:
        self.model.source = source.as_posix()

    @property
    def target(self) -> Path:
        return Path(self.model.target)

    @target.setter
    def target(self, target: Path) -> None:
        self.model.target = target.as_posix()
