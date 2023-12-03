"""Module containing various IO related functions."""
from __future__ import annotations

from pathlib import Path
from subprocess import CalledProcessError, check_call, check_output

from hwconfig.paths import get_data_dir
from hwconfig.platform import in_windows


def ensure_dir(directory: Path) -> Path:
    """Create the given directory if it does not already exist.

    Args:
        directory: The directory to create.

    Returns:
        The path of the created directory.
    """
    if not directory.exists():
        directory.mkdir(parents=True)

    return directory


def get_data_url() -> str:
    # TODO: Raise error if data url has not been set or is invalid.
    return NotImplemented


def set_data_url() -> None:
    # TODO: use "git ls-remote" to test access to repo as validation before writing to file.
    raise NotImplementedError


def clone_repo(src_url: str, dst_dir: Path, repo_dir_name: str = "") -> None:
    """Clone the repository at the given url to the given destination folder.

    Args:
        src_url: Url of the repo to clone.
        dst_dir: The directory to clone the repo to.
        repo_dir_name: Optional directory name for the Git repo (see Git clone options)
    """
    args = ["git", "clone", src_url]

    if repo_dir_name:
        args.append(repo_dir_name)

    check_call(args=args, shell=in_windows(), cwd=dst_dir)


def update_repo(repo_dir: Path) -> None:
    """Pull the repo in the given directory.

    Args:
        repo_dir: Path to the directory containing the repo to update.
    """
    args = ["git", "pull"]
    check_call(args=args, cwd=repo_dir, shell=in_windows())


def sync_config_data() -> None:
    """Sync the config data directory and return the local path to it."""
    config_data_dir = get_data_dir()

    if not config_data_dir.exists():
        ensure_dir(config_data_dir.parent)
        clone_repo(
            src_url=get_data_url(),
            dst_dir=config_data_dir.parent,
            repo_dir_name=config_data_dir.name,
        )
    else:
        update_repo(repo_dir=config_data_dir)


def get_powershell_dir() -> Path | None:
    """Get the PowerShell user directory located in <user_paths>/Documents/PowerShell.

    Returns:
        The path to the PowerShell directory if it exists, else None.
    """
    try:
        documents_dir = check_output(
            args=["powershell.exe", "[Environment]::GetFolderPath('MyDocuments')"],
            encoding="utf-8",
            shell=True,
        ).splitlines()[0]

    except CalledProcessError:
        return None

    powershell_dir = Path(documents_dir) / "PowerShell"
    if powershell_dir.exists():
        return powershell_dir

    return None
