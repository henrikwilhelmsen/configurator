from __future__ import annotations

from pydantic import BaseModel, Field


# TODO: Validate installer and platform
class InstallerModel(BaseModel):
    name: str = Field(default_factory=str)
    platform: str = Field(default_factory=str)
    installer: str = Field(default_factory=str)
    source: str = Field(default_factory=str)
    target: str = Field(default_factory=str)


class DataRepoModel(BaseModel):
    url: str
    manifest: str


class RepoManifestModel(BaseModel):
    installers: list[InstallerModel] = Field(default_factory=list)
