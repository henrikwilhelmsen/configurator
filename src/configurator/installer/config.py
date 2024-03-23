"""Module containing the installer config model."""
from pydantic import BaseModel, DirectoryPath


class InstallerConfig(BaseModel):
    """Installer config model."""

    name: str
    source: DirectoryPath
    target: DirectoryPath
