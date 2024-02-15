from pathlib import Path

import pytest
from result import Ok

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.terminal import TerminalInstaller


@pytest.fixture(name="mock_config")
def fixture_mock_config(test_terminal_source: Path, test_terminal_target: Path) -> InstallerConfig:
    return InstallerConfig(name="test", source=test_terminal_source, target=test_terminal_target)


@pytest.fixture(name="installer")
def fixture_installer(mock_config: InstallerConfig) -> TerminalInstaller:
    return TerminalInstaller(mock_config)


def test_install(installer: TerminalInstaller) -> None:
    result = installer.install()
    assert isinstance(result, Ok)


def test_uninstall(installer: TerminalInstaller) -> None:
    result = installer.uninstall()
    assert isinstance(result, Ok)
