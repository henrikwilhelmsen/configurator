from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


# TODO: Validate installer and platform
# TODO: Solution for target paths that need to be computed
# TODO: Field documentation
class InstallerConfig(BaseModel):
    name: str = Field(default_factory=str)
    platform: str = Field(default_factory=str)
    installer: str = Field(default_factory=str)
    source: Path = Field(default_factory=Path)
    target: Path = Field(default_factory=Path)
