"""hwconfig.installer.WindowsTerminalInstaller tests."""
from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2

import pytest

from hwconfig.config import InstallerConfig
from hwconfig.installer import WindowsTerminalInstaller
from hwconfig.result import Result


@pytest.fixture(name="win_terminal_source_file", scope="class")
def fixture_win_terminal_source_file() -> Path:
    """Get the path to the test data windows terminal settings file."""
    return Path(__file__).parent / "test_data" / "windows_terminal" / "source" / "terminal_settings.json"


@pytest.fixture(name="win_terminal_target_file", scope="class")
def fixture_win_terminal_target_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Get a copy of the target terminal settings file in a pytest temp dir."""
    tmp_dir = tmp_path_factory.mktemp("tmp")
    target_file = Path(__file__).parent / "test_data" / "windows_terminal" / "target" / "terminal_settings.json"
    copy2(src=target_file, dst=tmp_dir)
    return tmp_dir / "terminal_settings.json"


class TestWindowsTerminalInstaller:
    """Tests for the Windows Terminal installer."""

    @pytest.fixture(name="win_terminal_installer", scope="class")
    def fixture_win_terminal_installer(
        self,
        win_terminal_source_file: Path,
        win_terminal_target_file: Path,
        test_home_dir: Path,  # noqa: ARG002
    ) -> WindowsTerminalInstaller:
        """CopyDir installer configured with the test directories as source and target."""
        config = InstallerConfig(
            name="winterm_test",
            platform="Windows",
            installer="windows_terminal",
            source=win_terminal_source_file,
            target=win_terminal_target_file,
        )
        return WindowsTerminalInstaller(config)

    @pytest.fixture(name="backup", scope="class")
    def fixture_backup(
        self,
        win_terminal_installer: WindowsTerminalInstaller,
    ) -> tuple[WindowsTerminalInstaller, Result]:
        """Run the installer backup method and return the installer and result."""
        result = win_terminal_installer.backup()
        return (win_terminal_installer, result)

    @pytest.fixture(name="install", scope="class")
    def fixture_install(
        self,
        win_terminal_installer: WindowsTerminalInstaller,
    ) -> tuple[WindowsTerminalInstaller, Result]:
        """Run the installer install method and return the installer and result."""
        result = win_terminal_installer.install()
        return (win_terminal_installer, result)

    @pytest.fixture(name="uninstall", scope="class")
    def fixture_uninstall(
        self,
        win_terminal_installer: WindowsTerminalInstaller,
    ) -> tuple[WindowsTerminalInstaller, Result]:
        """Run the installer uninstall method and return the installer and result."""
        result = win_terminal_installer.uninstall()
        return (win_terminal_installer, result)

    def test_backup_result_ok(self, backup: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the backup method returns the expected result."""
        _, result = backup
        assert result == Result.OK

    def test_backup_files_match(self, backup: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the backed up files match the target directory."""
        installer, _ = backup
        backup_files = [x.name for x in installer.backup_dir.rglob("*")]
        target_files = [installer.config.target.name]
        assert backup_files == target_files

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_backup_exists_result_warning(self, win_terminal_installer: WindowsTerminalInstaller) -> None:
        """Check that the backup method returns warning as a result when the files already exist."""
        result = win_terminal_installer.backup()
        assert result == Result.WARNING

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_install_result_ok(self, install: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the install method returns the expected result."""
        _, result = install
        assert result == Result.OK

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_install_file_color_scheme(self, install: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the target colo scheme was updated."""
        installer, _ = install

        with installer.config.target.open() as f:
            target_data = json.load(f)

        assert target_data["profiles"]["defaults"]["colorScheme"] == "Dracula"

    @pytest.mark.depends(on=["test_backup_result_ok", "test_backup_files_match"])
    def test_install_file_always_show_tabs(self, install: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the target always show tabs setting was updated."""
        installer, _ = install

        with installer.config.target.open() as f:
            target_data = json.load(f)

        assert target_data["alwaysShowTabs"] is True

    @pytest.mark.depends(on=["test_install_result_ok"])
    def test_uninstall_result_ok(self, uninstall: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the uninstall method returns ok as a result."""
        _, result = uninstall
        assert result == Result.OK

    @pytest.mark.depends(on=["test_install_result_ok"])
    def test_uninstall_tabs_setting_reverted(self, uninstall: tuple[WindowsTerminalInstaller, Result]) -> None:
        """Check that the uninstall method restored the always show tabs setting."""
        installer, _ = uninstall

        with installer.config.target.open() as f:
            target_data = json.load(f)

        assert target_data["alwaysShowTabs"] is False
