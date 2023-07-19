"""hwconfig.installer.CopyInstaller tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from hwconfig.config import InstallerConfig
from hwconfig.installer import CopyInstaller
from hwconfig.result import Result


class TestCopyInstaller:
    """Tests for the CopyDir installer."""

    @pytest.fixture(name="copy_installer", scope="class")
    def fixture_copy_installer(
        self,
        test_source_dir: Path,
        test_target_dir: Path,
        test_home_dir: Path,  # noqa: ARG002
    ) -> CopyInstaller:
        """CopyDir installer configured with the test directories as source and target."""
        config = InstallerConfig(
            name="foo123",
            platform="Linux",
            installer="copy",
            source=test_source_dir,
            target=test_target_dir,
        )
        return CopyInstaller(config)

    @pytest.fixture(name="backup", scope="class")
    def fixture_backup(self, copy_installer: CopyInstaller) -> tuple[CopyInstaller, Result]:
        """Run the installer backup method and return the installer and result."""
        result = copy_installer.backup()
        return (copy_installer, result)

    @pytest.fixture(name="install", scope="class")
    def fixture_install(self, copy_installer: CopyInstaller) -> tuple[CopyInstaller, Result]:
        """Run the installer install method and return the installer and result."""
        result = copy_installer.install()
        return (copy_installer, result)

    @pytest.fixture(name="uninstall", scope="class")
    def fixture_uninstall(self, copy_installer: CopyInstaller) -> tuple[CopyInstaller, Result]:
        """Run the installer uninstall method and return the installer and result."""
        result = copy_installer.uninstall()
        return (copy_installer, result)

    def test_backup_result_ok(self, backup: tuple[CopyInstaller, Result]) -> None:
        """Check that the backup method returns the expected result."""
        _, result = backup
        assert result == Result.OK

    def test_backup_files_match(self, backup: tuple[CopyInstaller, Result]) -> None:
        """Check that the backed up files match the target directory."""
        installer, _ = backup
        backup_files = [x.name for x in installer.backup_dir.rglob("*")]
        target_files = [x.name for x in installer.config.target.rglob("*")]
        assert backup_files == target_files

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_backup_exists_result_warning(self, copy_installer: CopyInstaller) -> None:
        """Check that the backup method returns warning as a result when the files already exist."""
        result = copy_installer.backup()
        assert result == Result.WARNING

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_install_result_ok(self, install: tuple[CopyInstaller, Result]) -> None:
        """Check that the install method returns the expected result."""
        _, result = install
        assert result == Result.OK

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_install_files_match(self, install: tuple[CopyInstaller, Result]) -> None:
        """Check that the installed files match the source directory."""
        installer, _ = install
        source_files = [x.name for x in installer.config.source.rglob("*")]
        target_files = [x.name for x in installer.config.target.rglob("*")]
        assert source_files == target_files

    @pytest.mark.depends(on=["test_install_result_ok", "test_install_files_match"])
    def test_uninstall_result_ok(self, uninstall: tuple[CopyInstaller, Result]) -> None:
        """Check that the uninstall method returns ok as a result."""
        _, result = uninstall
        assert result == Result.OK

    @pytest.mark.depends(on=["test_install_result_ok", "test_install_files_match"])
    def test_uninstall_files_match(self, uninstall: tuple[CopyInstaller, Result]) -> None:
        """Check that the uninstall method restored the backed up files."""
        installer, _ = uninstall
        backup_files = [x.name for x in installer.backup_dir.rglob("*")]
        target_files = [x.name for x in installer.config.target.rglob("*")]
        assert backup_files == target_files
