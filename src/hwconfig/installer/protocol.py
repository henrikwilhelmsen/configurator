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
        """Install the config source files to the target directory."""
        ...

    def uninstall(self) -> Result[str, str]:
        """Delete the config files."""
        ...

    def write_to_source(self) -> Result[str, str]:
        """Write the target config files to the source directory."""
        ...
