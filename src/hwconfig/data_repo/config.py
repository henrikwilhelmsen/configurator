from pathlib import Path

from result import Result

from hwconfig.data_repo.model import DataRepoModel
from hwconfig.paths import get_data_dir


class DataRepoConfig:
    def __init__(self, model: DataRepoModel) -> None:
        self.model: DataRepoModel = model

    @property
    def url(self) -> str:
        """The url to the data git repository."""
        return self.model.url

    @url.setter
    def url(self, url: str) -> None:
        self.model.url = url

    @property
    def manifest(self) -> str:
        """The repo manifest file, relative to the repo root dir."""
        return self.model.manifest

    @manifest.setter
    def manifest(self, manifest: str) -> None:
        self.model.manifest = manifest

    @property
    def data_repo_dir(self) -> Path:
        """Path to the local data repo directory."""
        return get_data_dir()


def create_config_file(_: DataRepoConfig) -> Result[DataRepoConfig, str]:
    return NotImplemented


def get_config_from_file() -> Result[DataRepoConfig, str]:
    return NotImplemented
