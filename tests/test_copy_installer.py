from pathlib import Path
from unittest.mock import MagicMock

import pytest
from result import Err, Ok

from configurator.installer.config import InstallerConfig
from configurator.installer.copy import CopyInstaller


@pytest.fixture(name="mock_config")
def fixture_mock_config(test_source_dir: Path, test_target_dir: Path) -> InstallerConfig:
    return InstallerConfig(name="test", source=test_source_dir, target=test_target_dir)


@pytest.fixture(name="installer")
def fixture_installer(mock_config: InstallerConfig) -> CopyInstaller:
    return CopyInstaller(mock_config)


def test_install(installer: CopyInstaller) -> None:
    result = installer.install()
    assert isinstance(result, Ok)


def test_install_fail(monkeypatch: pytest.MonkeyPatch, installer: CopyInstaller) -> None:
    mock_copytree = MagicMock(side_effect=OSError("error"))
    monkeypatch.setattr("configurator.installer.copy.copytree", mock_copytree)
    result = installer.install()
    assert isinstance(result, Err)
