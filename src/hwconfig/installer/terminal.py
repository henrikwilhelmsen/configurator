"""Module containing the TerminalInstaller implementation."""
from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING

from hwconfig.installer.abstract import Installer
from hwconfig.io import ensure_dir
from hwconfig.result import Result

if TYPE_CHECKING:
    from hwconfig.installer.config import InstallerConfig


class TerminalInstaller(Installer):
    """Installer for Windows Terminal config."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize the installer with a config."""
        super().__init__(config)

        if not self.config.target:
            self.config.target = self._get_target_path()

    def install(self) -> Result:
        """Install terminal settings by copying relevant settings from source to the terminal settings file."""
        # load source and destination data
        with self.config.source.open() as file:
            source_data = json.load(file)
        with self.config.target.open() as file:
            destination_data = json.load(file)

        # update default settings
        destination_data["profiles"]["defaults"] = source_data["profiles"]["defaults"]

        # update schemes, only add/override schemes found in source data
        source_schemes: list[dict] = source_data["schemes"]
        destination_schemes: list[dict] = destination_data["schemes"]
        source_scheme_names = [x["name"] for x in source_schemes]

        # remove any destination scheme that exists in source schemes
        for n, scheme in enumerate(destination_schemes):
            if scheme["name"] in source_scheme_names:
                destination_schemes.pop(n)

        # add source schemes to destination schemes
        destination_schemes.extend(source_schemes)
        destination_data["schemes"] = destination_schemes

        # update application settings, not nested in destination only source
        source_application_data: dict = source_data["application"]

        for key, value in source_application_data.items():
            destination_data[key] = value

        # write to destination file
        with self.config.target.open("w", encoding="utf-8") as file:
            json.dump(destination_data, file)

        return Result.OK

    def uninstall(self) -> Result:
        """Uninstall the config file by deleting it and restoring the backup."""
        self.config.target.unlink()
        backup_file = self.backup_dir / self.config.target.name
        copy2(src=backup_file, dst=self.config.target)

        return Result.OK

    def backup(self) -> Result:
        """Create a backup of the target settings file if one does not exist."""
        if self.backup_dir.exists():
            return Result.WARNING

        ensure_dir(self.backup_dir)
        copy2(self.config.target, self.backup_dir)

        return Result.OK

    def _get_target_path(self) -> Path:
        return Path.home().joinpath(
            "AppData",
            "Local",
            "Packages",
            "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
            "LocalState",
            "settings.json",
        )
