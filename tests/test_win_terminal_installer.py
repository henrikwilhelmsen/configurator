from pathlib import Path

import pytest
from result import Ok

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.terminal import TerminalInstaller


@pytest.fixture(name="mock_config")
def fixture_mock_config(test_terminal_source_dir: Path, test_terminal_target_dir: Path) -> InstallerConfig:
    return InstallerConfig(name="test", source=test_terminal_source_dir, target=test_terminal_target_dir)


@pytest.fixture(name="installer")
def fixture_installer(mock_config: InstallerConfig) -> TerminalInstaller:
    return TerminalInstaller(mock_config)


def test_install(installer: TerminalInstaller) -> None:
    result = installer.install()
    assert isinstance(result, Ok)
