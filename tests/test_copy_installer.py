"""Copy installer tests."""
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from result import Err, Ok

from configurator.installer.config import InstallerConfig
from configurator.installer.copy import CopyInstaller


@pytest.fixture(name="mock_config")
def fixture_mock_config(
    test_source_dir: Path,
    test_target_dir: Path,
) -> InstallerConfig:
    """Fixture containing a mock InstallerConfig.

    Args:
        test_source_dir: Fixture containing the path to the test source data directory.
        test_target_dir: Fixture containing the path to the test target data directory.

    Returns:
        A mock InstallerConfig.
    """
    return InstallerConfig(name="test", source=test_source_dir, target=test_target_dir)


@pytest.fixture(name="installer")
def fixture_installer(mock_config: InstallerConfig) -> CopyInstaller:
    """A mock CopyInstaller.

    Args:
        mock_config: Fixture containing a mock InstallerConfig.

    Returns:
        A mock CopyInstaller.
    """
    return CopyInstaller(mock_config)


def test_install(installer: CopyInstaller) -> None:
    """Test installing the config files."""
    result = installer.install()
    assert isinstance(result, Ok)


def test_install_fail(
    monkeypatch: pytest.MonkeyPatch,
    installer: CopyInstaller,
) -> None:
    """Test installing the config files when the copy fails."""
    mock_copytree = MagicMock(side_effect=OSError("error"))
    monkeypatch.setattr("configurator.installer.copy.copytree", mock_copytree)
    result = installer.install()
    assert isinstance(result, Err)
