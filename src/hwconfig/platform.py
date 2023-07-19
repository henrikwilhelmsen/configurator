"""Platform related utility functions."""
import platform


def in_wsl() -> bool:
    """Check if we are running in a WSL instance."""
    return "microsoft-standard" in platform.uname().release


def in_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"
