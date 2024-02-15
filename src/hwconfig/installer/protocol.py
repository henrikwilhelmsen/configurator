from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from result import Result

    from hwconfig.installer.config import InstallerConfig


class Installer(Protocol):
    @property
    def config(self) -> InstallerConfig:
        ...

    def install(self) -> Result[str, str]:
        """Install the config source files."""
        ...

    def uninstall(self) -> Result[str, str]:
        """Uninstall the config files and restore the backup."""
        ...
