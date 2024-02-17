from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from result import Err, Ok, Result

from hwconfig.util import get_json_data_from_file

if TYPE_CHECKING:
    from pathlib import Path

    from hwconfig.installer.config import InstallerConfig


class TerminalInstaller:
    """Installer for Windows Terminal config.

    Windows Terminal has a lot of settings that are system specific, and all of them are in a single file.
    Therefore only the settings that we would like to have shared are stored in the source file, and then written
    to the target config without removing or affecting any other settings.
    """

    def __init__(self, config: InstallerConfig) -> None:
        self.config: InstallerConfig = config

    def _get_source_settings_file(self) -> Result[Path, str]:
        source_file = self.config.source / "settings.json"
        if not source_file.exists():
            return Err(f"Could not find source file at {source_file}")

        return Ok(source_file)

    def _get_target_settings_file(self) -> Result[Path, str]:
        target_file = self.config.target / "settings.json"

        if not target_file.exists():
            return Err(f"Could not find target file at {target_file}")

        return Ok(target_file)

    def _get_source_and_target_json_data(
        self,
        source_file: Path,
        target_file: Path,
    ) -> Result[tuple[dict[Any, Any], dict[Any, Any]], str]:
        """Install terminal settings by copying relevant settings from source to the terminal settings file."""
        source_data_result = get_json_data_from_file(file=source_file)
        destination_data_result = get_json_data_from_file(file=target_file)

        match source_data_result, destination_data_result:
            case (Err(e), _):
                return Err(f"Could not read source file: {e}")
            case (_, Err(e)):
                return Err(f"Could not read destination file: {e}")
            case (Ok(source_data), Ok(destination_data)):
                return Ok((source_data, destination_data))

        return Err("Unknown error occurred")

    def _copy_source_data_to_target(
        self,
        source_data: dict[Any, Any],
        target_data: dict[Any, Any],
    ) -> Result[dict[str, str], str]:
        # update default settings
        target_data["profiles"]["defaults"] = source_data["profiles"]["defaults"]

        # update schemes, only add/override schemes found in source data
        source_schemes: list[dict[Any, Any]] = source_data["schemes"]
        destination_schemes: list[dict[Any, Any]] = target_data["schemes"]
        source_scheme_names = [x["name"] for x in source_schemes]

        # remove any destination scheme that exists in source schemes
        for n, scheme in enumerate(destination_schemes):
            if scheme["name"] in source_scheme_names:
                destination_schemes.pop(n)

        # add source schemes to destination schemes
        destination_schemes.extend(source_schemes)
        target_data["schemes"] = destination_schemes

        # update application settings, not nested in destination only source
        source_application_data: dict[Any, Any] = source_data["application"]
        for key, value in source_application_data.items():
            target_data[key] = value

        return Ok(target_data)

    def _write_target_data_to_file(self, target_data: dict[Any, Any], target_file: Path) -> Result[str, str]:
        try:
            with target_file.open("w", encoding="utf-8") as file:
                json.dump(target_data, file)
                return Ok(f"Data written to {self.config.name} config file")

        except FileNotFoundError as e:
            return Err(f"Failed to write to {self.config.name} config file: {e}")

        except PermissionError as e:
            return Err(f"Failed to write to {self.config.name} config file: {e}")

    def install(self) -> Result[str, str]:  # noqa: PLR0911
        """Install terminal settings by copying relevant settings from source to the terminal settings file."""
        source_file_result = self._get_source_settings_file()
        target_file_result = self._get_target_settings_file()

        match source_file_result, target_file_result:
            case (Err(_), _):
                return source_file_result
            case (_, Err(_)):
                return target_file_result
            case (Ok(source_val), Ok(target_val)):
                source_file = source_val
                target_file = target_val
                data_result = self._get_source_and_target_json_data(source_file=source_file, target_file=target_file)

        match data_result:
            case Err(_):
                return data_result
            case Ok((source_data, destination_data)):
                copy_data_result = self._copy_source_data_to_target(source_data, destination_data)

        match copy_data_result:
            case Err(_):
                return copy_data_result
            case Ok(target_data):
                write_file_result = self._write_target_data_to_file(target_data, target_file=target_file)

        match write_file_result:
            case Err(_):
                return write_file_result
            case Ok(v):
                return Ok(v)

        return Err("Unknown error occurred")

    def write_to_source(self) -> Result[str, str]:
        return Err("Terminal config does not support writing to source yet.")
