"""hwconfig.installer.WindowsTerminalInstaller tests."""
from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2

import pytest
from result import Result, is_err, is_ok

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.terminal import TerminalInstaller
from hwconfig.settings import Settings


@pytest.fixture(name="terminal_source_file", scope="class")
def fixture_terminal_source_file() -> Path:
    """Get the path to the test data windows terminal settings file."""
    return Path(__file__).parent / "test_data" / "windows_terminal" / "repo_source" / "settings.json"


@pytest.fixture(name="terminal_target_file", scope="class")
def fixture_terminal_target_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Get a copy of the target terminal settings file in a pytest temp dir."""
    tmp_dir = tmp_path_factory.mktemp("tmp")
    target_file = Path(__file__).parent / "test_data" / "windows_terminal" / "local_target" / "settings.json"
    copy2(src=target_file, dst=tmp_dir)
    return tmp_dir / "settings.json"


class TestTerminalInstaller:
    """Tests for the Windows Terminal installer."""

    @pytest.fixture(name="settings", scope="class")
    def fixture_settings(self, tmp_path_class: Path) -> Settings:
        return Settings(home_dir=tmp_path_class / ".hwconfig")

    @pytest.fixture(name="terminal_installer", scope="class")
    def fixture_terminal_installer(
        self,
        terminal_source_file: Path,
        terminal_target_file: Path,
        tmp_path_class: Path,
        settings: Settings,
    ) -> TerminalInstaller:
        """Create and return  a Windows Terminal installer instance."""
        config = InstallerConfig(
            name="winterm_test",
            platform="Windows",
            installer="windows_terminal",
            source=terminal_source_file,
            target=terminal_target_file,
        )
        config = InstallerConfig()
        return TerminalInstaller(config, settings)

    @pytest.fixture(name="backup", scope="class")
    def fixture_backup(self, terminal_installer: TerminalInstaller) -> Result:
        """Run the installer backup method and return the result."""
        return terminal_installer.backup()

    @pytest.fixture(name="install", scope="class")
    def fixture_install(self, terminal_installer: TerminalInstaller) -> Result:
        """Run the installer install method and return the result."""
        return terminal_installer.install()

    @pytest.fixture(name="uninstall", scope="class")
    def fixture_uninstall(self, install: Result, terminal_installer: TerminalInstaller) -> Result:  # noqa: ARG002
        """Run the installer uninstall method and return the installer and result."""
        return terminal_installer.uninstall()

    def test_backup_result_ok(self, backup: Result) -> None:
        assert is_ok(backup)

    def test_backup_files_match(self, backup: Result, terminal_installer: TerminalInstaller) -> None:  # noqa: ARG002
        """Check that the backed up files match the target directory."""
        backup_files = [x.name for x in terminal_installer.config.backup_dir.rglob("*")]
        target_files = [terminal_installer.config.target.name]
        assert backup_files == target_files

    def test_install_result_ok(self, install: Result) -> None:
        assert is_ok(install)

    def test_install_file_color_scheme(self, install: Result, terminal_installer: TerminalInstaller) -> None:  # noqa: ARG002
        """Check that the target colo scheme was updated."""
        with terminal_installer.config.target.open() as f:
            target_data = json.load(f)

        assert target_data["profiles"]["defaults"]["colorScheme"] == "Dracula"

    def test_install_file_always_show_tabs(self, install: Result, terminal_installer: TerminalInstaller) -> None:  # noqa: ARG002
        """Check that the target always show tabs setting was updated."""
        with terminal_installer.config.target.open() as f:
            target_data = json.load(f)

        assert target_data["alwaysShowTabs"] is True

    def test_uninstall_result_ok(self, uninstall: Result) -> None:
        """Check that the uninstall method returns ok as a result."""
        assert is_ok(uninstall)

    def test_uninstall_tabs_setting_reverted(self, uninstall: Result, terminal_installer: TerminalInstaller) -> None:  # noqa: ARG002
        """Check that the uninstall method restored the always show tabs setting."""
        with terminal_installer.config.target.open() as f:
            target_data = json.load(f)

        with pytest.raises(KeyError):
            _ = target_data["alwaysShowTabs"]
