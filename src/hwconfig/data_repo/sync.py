from subprocess import call

from result import Err, Ok, Result

from hwconfig.data_repo.config import DataRepoConfig
from hwconfig.util import ensure_dir, in_windows


def _clone_repo(config: DataRepoConfig) -> Result[DataRepoConfig, int]:
    ensure_dir(config.data_repo_dir.parent)

    args = ["git", "clone", config.url, config.data_repo_dir.name]
    returncode = call(args=args, shell=in_windows(), cwd=config.data_repo_dir.parent)

    if returncode != 0:
        return Err(returncode)

    return Ok(config)


def _update_repo(config: DataRepoConfig) -> Result[DataRepoConfig, int]:
    args = ["git", "pull"]
    returncode = call(args=args, cwd=config.data_repo_dir, shell=in_windows())

    if returncode != 0:
        return Err(returncode)

    return Ok(config)


def sync_data_repo(config: DataRepoConfig) -> Result[DataRepoConfig, int]:
    """Sync the config data repo."""
    if not config.data_repo_dir.exists():
        return _clone_repo(config=config)

    return _update_repo(config=config)
