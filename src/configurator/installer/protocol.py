"""Installer protocol module."""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from result import Result

    from configurator.installer.config import InstallerConfig


class Installer(Protocol):
    """Installer protocol."""

    @property
    def config(self) -> InstallerConfig:
        """The config for the installer.

        Returns:
            The config for the installer.
        """
        ...

    def install(self) -> Result[str, str]:
        """Write the source config to the target directory.

        Returns:
            A result containing a success message or an error message.
        """
        ...

    def write_to_source(self) -> Result[str, str]:
        """Write the target config files back to the source directory.

        Returns:
            A result containing a success message or an error message.
        """
        ...
