from __future__ import annotations

from shutil import copytree, rmtree
from typing import TYPE_CHECKING

from result import Err, Ok, Result

from hwconfig.util import ensure_dir

if TYPE_CHECKING:
    from hwconfig.installer.config import InstallerConfig


class CopyInstaller:
    """Installer for config files that only need to be copied to a target location."""

    def __init__(self, config: InstallerConfig) -> None:
        self.config: InstallerConfig = config

    def install(self) -> Result[str, str]:
        """Install the config files by copying source dir to target."""
        try:
            ensure_dir(self.config.target)
            copytree(src=self.config.source, dst=self.config.target, dirs_exist_ok=True)
        except OSError as e:
            return Err(f"Failed to install {self.config.name} config: {e}")

        return Ok(f"Installed {self.config.name} config files")

    def uninstall(self) -> Result[str, str]:
        """Uninstall the config files by deleting them and restoring the backup."""
        try:
            rmtree(self.config.target)
        except OSError as e:
            return Err(f"Failed to remove {self.config.name} config: {e}")

        return Ok(f"Removed {self.config.name} config files.")
