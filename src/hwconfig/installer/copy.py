"""Module containing the CopyInstaller implementation."""
from shutil import copytree, rmtree

from hwconfig.installer.abstract import Installer
from hwconfig.installer.config import InstallerConfig
from hwconfig.io import ensure_dir
from hwconfig.result import Result


class CopyInstaller(Installer):
    """Installer for config files that only need to be copied to a target location."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize copy installer with a config."""
        super().__init__(config)

    def install(self) -> Result:
        """Install the config files by copying source dir to target."""
        ensure_dir(self.config.target)
        copytree(src=self.config.source, dst=self.config.target, dirs_exist_ok=True)

        return Result.OK

    def uninstall(self) -> Result:
        """Uninstall the config files by deleting them and restoring the backup."""
        rmtree(self.config.target)
        copytree(src=self.backup_dir, dst=self.config.target)

        return Result.OK

    def backup(self) -> Result:
        """Create a backup of the target directory if one does not exist."""
        if self.backup_dir.exists():
            return Result.WARNING

        ensure_dir(self.backup_dir.parent)
        copytree(src=self.config.target, dst=self.backup_dir)

        return Result.OK
