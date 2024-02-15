from pathlib import Path

from pydantic import BaseModel


class InstallerConfig(BaseModel):
    name: str
    source: Path
    target: Path
