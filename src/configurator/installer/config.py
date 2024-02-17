from pydantic import BaseModel, DirectoryPath


class InstallerConfig(BaseModel):
    name: str
    source: DirectoryPath
    target: DirectoryPath
