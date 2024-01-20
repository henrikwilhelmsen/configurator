from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_home_dir() -> Path:
    """Get the path to the default hwconfig home directory."""
    return Path.home() / ".hwconfig"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HWCONFIG_")
    home_dir: Path = Field(default=get_home_dir())

    @computed_field
    @property
    def data_dir(self) -> Path:
        return self.home_dir / "data"

    @computed_field
    @property
    def backup_dir(self) -> Path:
        return self.home_dir / "backup"

    @computed_field
    @property
    def data_config_file(self) -> Path:
        return self.home_dir / "data_config.json"
