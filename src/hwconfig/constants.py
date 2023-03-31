import os
from pathlib import Path


def get_hwconfig_home_dir() -> Path:
    hwconfig_home_env = os.getenv("HWCONFIG_HOME")

    if hwconfig_home_env:
        return Path(hwconfig_home_env)

    return Path.home() / ".hwconfig"


def get_config_data_url() -> str:
    source_env = os.getenv("HWCONFIG_DATA_SOURCE")
    if source_env:
        return source_env

    return "https://github.com/henrikwilhelmsen/hw-config-data.git"
