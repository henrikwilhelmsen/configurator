"""Module containing the CopyInstaller implementation."""
from pathlib import Path
from shutil import copytree, rmtree

from result import Err, Ok, Result

from hwconfig.installer.abstract import Installer
from hwconfig.installer.config import InstallerConfig
from hwconfig.settings import Settings
from hwconfig.util import ensure_dir


class CopyInstaller(Installer):
    """Installer for config files that only need to be copied to a target location."""

    def __init__(self, config: InstallerConfig, settings: Settings) -> None:
        """Initialize copy installer with a config."""
        super().__init__(config=config, settings=settings)

    def backup_dir(self) -> Path:
        """Get the path to the installer specific backup directory."""
        return self.settings.backup_dir / self.config.name

    def install(self) -> Result[str, str]:
        """Install the config files by copying source dir to target."""
        if not self.backup_dir().exists():
            backup_result = self.backup()

            if not backup_result.is_ok():
                return Err(f"Could not create backup: {backup_result.unwrap_err()}")

        ensure_dir(self.config.target)
        copytree(src=self.config.source, dst=self.config.target, dirs_exist_ok=True)

        return Ok(f"Installed {self.config.name} config files")

    def uninstall(self) -> Result[str, str]:
        """Uninstall the config files by deleting them and restoring the backup."""
        if not self.backup_dir().exists():
            return Err(f"Backup directory does not exist: {self.backup_dir}")

        rmtree(self.config.target)
        copytree(src=self.backup_dir(), dst=self.config.target)

        return Ok(f"Uninstalled {self.config.name} config files and reverted to backup.")

    def backup(self) -> Result[str, str]:
        """Create a backup of the target directory."""
        ensure_dir(self.backup_dir().parent)
        copytree(src=self.config.target, dst=self.backup_dir())

        return Ok(f"Created backup of {self.config.name} config files")
