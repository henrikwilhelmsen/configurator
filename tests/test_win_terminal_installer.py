"""Windows Terminal installer tests."""
from pathlib import Path

import pytest
from result import Ok

from configurator.installer.config import InstallerConfig
from configurator.installer.terminal import TerminalInstaller


@pytest.fixture(name="mock_config")
def fixture_mock_config(
    test_terminal_source_dir: Path,
    test_terminal_target_dir: Path,
) -> InstallerConfig:
    """Mock InstallerConfig.

    Args:
        test_terminal_source_dir: Fixture containing the path to the test source dir.
        test_terminal_target_dir: Fixture containing the path to the test target dir.

    Returns:
        A mock InstallerConfig.
    """
    return InstallerConfig(
        name="test",
        source=test_terminal_source_dir,
        target=test_terminal_target_dir,
    )


@pytest.fixture(name="installer")
def fixture_installer(mock_config: InstallerConfig) -> TerminalInstaller:
    """Mock TerminalInstaller.

    Args:
        mock_config: Fixture containing a mock InstallerConfig.

    Returns:
        A mock TerminalInstaller.
    """
    return TerminalInstaller(mock_config)


def test_install(installer: TerminalInstaller) -> None:
    """Test installing the config files."""
    result = installer.install()
    assert isinstance(result, Ok)
