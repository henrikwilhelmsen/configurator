"""Module containing the TerminalInstaller implementation."""
from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING, Any

from result import Err, Ok, Result

from hwconfig.installer.abstract import Installer
from hwconfig.settings import Settings
from hwconfig.util import check_file_exists, ensure_dir, get_json_data_from_file

if TYPE_CHECKING:
    from hwconfig.installer.config import InstallerConfig


class TerminalInstaller(Installer):
    """Installer for Windows Terminal config."""

    def __init__(self, config: InstallerConfig, settings: Settings) -> None:
        """Initialize the installer with a config."""
        super().__init__(config=config, settings=settings)

        if not self.config.target:
            self.config.target = self._get_target_path()

    def backup_dir(self) -> Path:
        return self.settings.backup_dir / self.config.name

    @property
    def backup_file(self) -> Path:
        return self.backup_dir() / "settings.json"

    def _ensure_source_and_target_files(self) -> Result[str, str]:
        """Ensure that the source and target paths exist and are files, not directories."""
        if self.config.source.is_dir():
            source_result = check_file_exists(self.config.source / "settings.json")
        else:
            source_result = check_file_exists(self.config.source)

        if self.config.target.is_dir():
            target_result = check_file_exists(self.config.target / "settings.json")
        else:
            target_result = check_file_exists(self.config.target)

        match source_result, target_result:
            case (Err(e), _):
                return Err(f"Could not find source file: {e}")
            case (_, Err(e)):
                return Err(f"Could not find target file: {e}")
            case (Ok(source_file), Ok(target_file)):
                self.config.source = source_file
                self.config.target = target_file
                return Ok("Source and target files found")

        return Err("Unknown error occurred")

    def _get_source_and_target_json_data(self) -> Result[tuple[dict[Any, Any], dict[Any, Any]], str]:
        """Install terminal settings by copying relevant settings from source to the terminal settings file."""
        source_data_result = get_json_data_from_file(file=self.config.source)
        destination_data_result = get_json_data_from_file(file=self.config.target)

        match source_data_result, destination_data_result:
            case (Err(e), _):
                return Err(f"Could not read source file: {e}")
            case (_, Err(e)):
                return Err(f"Could not read destination file: {e}")
            case (Ok(source_data), Ok(destination_data)):
                return Ok((source_data, destination_data))

        return Err("Unknown error occurred")

    # TODO: Add error paths and try/except blocks
    def _copy_source_data_to_target(
        self,
        source_data: dict[Any, Any],
        target_data: dict[Any, Any],
    ) -> Result[dict[str, str], str]:
        # update default settings
        target_data["profiles"]["defaults"] = source_data["profiles"]["defaults"]

        # update schemes, only add/override schemes found in source data
        source_schemes: list[dict] = source_data["schemes"]
        destination_schemes: list[dict] = target_data["schemes"]
        source_scheme_names = [x["name"] for x in source_schemes]

        # remove any destination scheme that exists in source schemes
        for n, scheme in enumerate(destination_schemes):
            if scheme["name"] in source_scheme_names:
                destination_schemes.pop(n)

        # add source schemes to destination schemes
        destination_schemes.extend(source_schemes)
        target_data["schemes"] = destination_schemes

        # update application settings, not nested in destination only source
        source_application_data: dict = source_data["application"]
        for key, value in source_application_data.items():
            target_data[key] = value

        return Ok(target_data)

    def _write_target_data_to_file(self, target_data: dict) -> Result[str, str]:
        with self.config.target.open("w", encoding="utf-8") as file:
            json.dump(target_data, file)
            return Ok(f"Updated {self.config.name} config file")

    # TODO: Break this method up into smaller methods
    def install(self) -> Result[str, str]:
        """Install terminal settings by copying relevant settings from source to the terminal settings file."""
        if not self.backup_file.exists():
            backup_result = self.backup()

            if backup_result.is_err():
                return backup_result

        ensure_files_result = self._ensure_source_and_target_files()
        if ensure_files_result.is_err():
            return ensure_files_result

        data_result = self._get_source_and_target_json_data()
        match data_result:
            case Err(_):
                return data_result
            case Ok((source_data, destination_data)):
                copy_data_result = self._copy_source_data_to_target(source_data, destination_data)

        match copy_data_result:
            case Err(_):
                return copy_data_result
            case Ok(target_data):
                write_file_result = self._write_target_data_to_file(target_data)

        match write_file_result:
            case Err(_):
                uninstall_result = self.uninstall()
                if uninstall_result.is_err():
                    return uninstall_result

                return write_file_result
            case Ok(_):
                return Ok(f"Installed {self.config.name} config file")

        return Err("Unknown error occurred")

    def uninstall(self) -> Result:
        """Uninstall the config file by deleting it and restoring the backup."""
        ensure_files_result = self._ensure_source_and_target_files()

        if ensure_files_result.is_err():
            return ensure_files_result

        if not self.config.backup_dir.exists():
            return Err(f"{self.config.name} backup does not exist, nothing to revert to.")

        self.config.target.unlink()
        copy2(src=self.backup_file, dst=self.config.target)

        return Ok(f"Uninstalled {self.config.name} config file and restored backup.")

    def backup(self) -> Result:
        """Back up the target file to the backup directory."""
        ensure_dir(self.config.backup_dir)
        copy2(self.config.target, self.backup_file)

        return Ok(f"Created backup of {self.config.name} config file")

    def _get_target_path(self) -> Path:
        return Path.home().joinpath(
            "AppData",
            "Local",
            "Packages",
            "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
            "LocalState",
            "settings.json",
        )
