from __future__ import annotations

from pydantic import BaseModel, Field

from hwconfig.installer.model import InstallerModel


class DataRepoModel(BaseModel):
    url: str
    manifest: str


class RepoManifestModel(BaseModel):
    installers: list[InstallerModel] = Field(default_factory=list)
