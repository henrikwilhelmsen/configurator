"""Module containing config model classes."""
from __future__ import annotations

from pathlib import Path  # noqa: TCH003

from pydantic import BaseModel

# TODO: Tests


class InstallerConfig(BaseModel):
    """Installer config model, contains all settings required by an installer."""

    # TODO: Custom validation for installer and platform
    # TODO: Can source and target be Path objects?

    name: str
    platform: str
    installer: str
    source: Path
    target: Path


class DataConfig(BaseModel):
    """Data config model, contains all settings for the data repository."""

    installer_configs: list[InstallerConfig]
