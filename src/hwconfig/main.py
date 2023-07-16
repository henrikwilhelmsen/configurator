from hwconfig.result import Report


def install() -> Report:
    """Install config files."""
    return NotImplemented


def uninstall() -> Report:
    """Uninstall config files."""
    return NotImplemented


def set_data_url(url: str) -> Report:
    """Set the url to the data repository."""
    return NotImplemented
