from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from pydantic import BaseModel


# TODO: Custom validation for installer and platform
class InstallerConfig(BaseModel):
    name: str
    platform: str
    installer: str
    source: Path
    target: Path


class DataConfig(BaseModel):
    installer_configs: list[InstallerConfig]
