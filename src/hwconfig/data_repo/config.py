from hwconfig.models import DataRepoModel


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
