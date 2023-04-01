import os
from pathlib import Path

DATA_DIR_NAME = "config_data"


def get_hwconfig_home_dir() -> Path:
    """Get the path to the hwconfig home dir, from either an env var or a default.

    Returns:
        The path of the hwconfig home directory.
    """
    hwconfig_home_env = os.getenv("HWCONFIG_HOME")

    if hwconfig_home_env:
        return Path(hwconfig_home_env)

    return Path.home() / ".hwconfig"


def get_config_data_url() -> str:
    """Get the path to the hwconfig data repo, from either an env var or a default.

    Returns:
        The a string containing the url of the config data repository.
    """
    source_env = os.getenv("HWCONFIG_DATA_SOURCE")
    if source_env:
        return source_env

    return "https://github.com/henrikwilhelmsen/hw-config-data.git"
