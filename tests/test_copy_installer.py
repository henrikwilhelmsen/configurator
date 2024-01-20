"""hwconfig.installer.CopyInstaller tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hwconfig.settings import Settings

if TYPE_CHECKING:
    from pathlib import Path

import platform

import pytest
from result import Result, is_ok

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.copy import CopyInstaller


class TestCopyInstaller:
    """Tests for the CopyDir installer."""

    @pytest.fixture(name="settings", scope="class")
    def fixture_settings(self, tmp_path_class: Path) -> Settings:
        return Settings(home_dir=tmp_path_class / ".hwconfig")

    @pytest.fixture(name="copy_installer", scope="class")
    def fixture_copy_installer(
        self,
        test_source_dir: Path,
        test_target_dir: Path,
        settings: Settings,
    ) -> CopyInstaller:
        """CopyDir installer configured with the test directories as source and target."""
        config = InstallerConfig(
            name="test",
            platform=platform.system(),
            installer="copy",
            source=test_source_dir,
            target=test_target_dir,
        )
        return CopyInstaller(config=config, settings=settings)

    @pytest.fixture(name="backup", scope="class")
    def fixture_backup(self, copy_installer: CopyInstaller) -> Result[str, str]:
        """Run the installer backup method and return the installer and result."""
        return copy_installer.backup()

    @pytest.fixture(name="install", scope="class")
    def fixture_install(self, copy_installer: CopyInstaller) -> Result[str, str]:
        """Run the installer install method and return the installer and result."""
        return copy_installer.install()

    @pytest.fixture(name="uninstall", scope="class")
    def fixture_uninstall(self, install: Result[str, str], copy_installer: CopyInstaller) -> Result[str, str]:
        """Run the installer uninstall method and return the installer and result."""
        return copy_installer.uninstall()

    def test_backup_result_ok(self, backup: Result[str, str]) -> None:
        """Check that the backup method returns the expected result."""
        assert is_ok(backup)

    def test_backup_files_match(self, backup: Result[str, str], copy_installer: CopyInstaller) -> None:  # noqa: ARG002
        """Check that the backed up files match the target directory."""
        backup_files = [x.name for x in copy_installer.backup_dir().rglob("*")]
        target_files = [x.name for x in copy_installer.config.target.rglob("*")]
        assert backup_files == target_files

    def test_install_result_ok(self, install: Result[str, str]) -> None:
        """Check that the install method returns the expected result."""
        assert is_ok(install)

    def test_install_files_match(self, install: Result[str, str], copy_installer: CopyInstaller) -> None:  # noqa: ARG002
        """Check that the installed files match the source directory."""
        source_files = [x.name for x in copy_installer.config.source.rglob("*")]
        target_files = [x.name for x in copy_installer.config.target.rglob("*")]
        assert source_files == target_files

    def test_uninstall_result_ok(self, uninstall: Result[str, str]) -> None:
        """Check that the uninstall method returns ok as a result."""
        assert is_ok(uninstall)

    def test_uninstall_files_match(self, uninstall: Result[str, str], copy_installer: CopyInstaller) -> None:  # noqa: ARG002
        """Check that the uninstall method restored the backed up files."""
        backup_files = [x.name for x in copy_installer.backup_dir().rglob("*")]
        target_files = [x.name for x in copy_installer.config.target.rglob("*")]
        assert backup_files == target_files
