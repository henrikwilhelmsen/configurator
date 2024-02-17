from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HWCONFIG_")
    data_repo_url: str = "https://github.com/henrikwilhelmsen/config-files.git"

    @computed_field
    @property
    def root_dir(self) -> Path:
        return Path().home() / ".hwconfig"

    @computed_field
    @property
    def data_repo_dir(self) -> Path:
        return self.root_dir / "data_repo"


Settings = _Settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return _Settings()
