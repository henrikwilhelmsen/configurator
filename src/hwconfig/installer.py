from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hwconfig.config import InstallerConfig

from abc import ABC, abstractmethod
from shutil import copytree

from hwconfig.io import ensure_dir
from hwconfig.result import Result


class Installer(ABC):
    def __init__(self, config: InstallerConfig):
        self.config: InstallerConfig = config

    @abstractmethod
    def install(self: Installer) -> Result:
        ...

    @abstractmethod
    def uninstall(self: Installer) -> Result:
        ...

    @abstractmethod
    def backup(self: Installer) -> Result:
        ...


class CopyDir(Installer):
    def __init__(self, config: InstallerConfig) -> None:
        super().__init__(config)

    def install(self) -> Result:
        """Install the config files by copying source dir to target."""
        ensure_dir(self.config.target)
        copytree(src=self.config.source, dst=self.config.source, dirs_exist_ok=True)

        return Result.OK

    def uninstall(self) -> Result:
        return NotImplemented

    def backup(self) -> Result:
        return NotImplemented


class WindowsTerminal(Installer):
    def __init__(self, config: InstallerConfig) -> None:
        super().__init__(config)

    def install(self) -> Result:
        return NotImplemented

    def uninstall(self) -> Result:
        return NotImplemented

    def backup(self) -> Result:
        return NotImplemented


INSTALLER_MAP = {
    "copy": CopyDir,
    "windows_terminal": WindowsTerminal,
}


async def get_installers(configs: list[InstallerConfig]) -> list[Installer]:
    return NotImplemented
