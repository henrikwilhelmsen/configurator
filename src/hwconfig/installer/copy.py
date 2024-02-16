from __future__ import annotations

from shutil import copy2, copytree, rmtree
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

    def write_to_source(self) -> Result[str, str]:
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
