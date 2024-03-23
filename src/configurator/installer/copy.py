"""Module containing the copy installer."""
from __future__ import annotations

from shutil import copy2, copytree
from typing import TYPE_CHECKING

from result import Err, Ok, Result

from configurator.util import ensure_dir

if TYPE_CHECKING:
    from configurator.installer.config import InstallerConfig


class CopyInstaller:
    """Installer for config files that only need to be copied to a target location."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize the installer.

        Args:
            config: Config for the installer.
        """
        self.config: InstallerConfig = config

    def install(self) -> Result[str, str]:
        """Install the config source files to the target directory.

        Returns:
            A result containing a success message or an error message.
        """
        try:
            ensure_dir(self.config.target)
            copytree(src=self.config.source, dst=self.config.target, dirs_exist_ok=True)
        except OSError as e:
            return Err(f"Failed to install {self.config.name} config: {e}")

        return Ok(f"Installed {self.config.name} config files")

    def write_to_source(self) -> Result[str, str]:
        """Write the target config files back to the source directory.

        Returns:
            A result containing a success message or an error message.
        """
        source_names = [p.name for p in self.config.source.glob("*")]
        target_paths = list(self.config.target.glob("*"))
        matched_paths = [p for p in target_paths if p.name in source_names]

        try:
            for p in matched_paths:
                if p.is_dir():
                    copytree(src=p, dst=self.config.source / p.name, dirs_exist_ok=True)
                else:
                    copy2(src=p, dst=self.config.source / p.name)
        except OSError as e:
            return Err(f"Failed to write to {self.config.name} source: {e}")

        return Ok(f"Copied {self.config.name} target file to source")
