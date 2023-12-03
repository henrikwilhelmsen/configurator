import os
from pathlib import Path


def get_home_dir() -> Path:
    """Get the path to the hwconfig home directory."""
    env_var = os.getenv("HWCONFIG_HOME_DIR")

    if env_var:
        return Path(env_var)

    return Path.home() / ".hwconfig"


def get_data_dir() -> Path:
    """Get the path to the hwconfig data directory."""
    env_var = os.getenv("HWCONFIG_DATA_DIR")

    if env_var:
        return Path(env_var)

    return get_home_dir().joinpath("data")


def get_backup_dir() -> Path:
    """Get the path to the hwconfig backup directory."""
    env_var = os.getenv("HWCONFIG_BACKUP_DIR")

    if env_var:
        return Path(env_var)

    return get_home_dir().joinpath("backup")


def get_data_config_file() -> Path:
    return get_home_dir() / "data_config.json"
