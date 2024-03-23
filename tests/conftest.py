"""Shared test code."""

from __future__ import annotations

from pathlib import Path
from shutil import copy2

import pytest

TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(name="test_source_dir")
def test_source_dir() -> Path:
    """Fixture containing the path to the test data directory.."""
    return Path(__file__).parent / "test_data" / "copy_dir"


@pytest.fixture(name="test_target_dir")
def fixture_test_target_dir(tmp_path: Path) -> Path:
    """A tmp directory to use as the target for installer tests."""
    tmp_file = tmp_path / "hello.json"
    tmp_file.touch()
    return tmp_path


@pytest.fixture(name="test_terminal_source_dir")
def fixture_test_terminal_source() -> Path:
    """Fixture containing the path to the test terminal data directory."""
    return Path(__file__).parent / "test_data" / "terminal_source"


@pytest.fixture(name="test_terminal_target_dir")
def fixture_test_terminal_target_dir(tmp_path: Path) -> Path:
    """A tmp directory to use as the target for installer tests."""
    tmp_file = tmp_path / "settings.json"
    target_file = TEST_DATA_DIR / "terminal_target.json"
    copy2(target_file, tmp_file)
    return tmp_path


@pytest.fixture(name="test_home_dir", scope="class")
def fixture_test_home_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty tmp directory to use as the hwconfig home dir, for tests."""
    monkeypatch.setenv("HWCONFIG_ROOT_DIR", tmp_path.as_posix())
    return tmp_path
