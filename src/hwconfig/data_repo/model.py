from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from hwconfig.installer.config import InstallerConfig


class DataRepoModel(BaseModel):
    url: str
    manifest: str


class RepoManifestModel(BaseModel):
    installers: list[InstallerConfig] = Field(default_factory=list)
