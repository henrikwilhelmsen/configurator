"""Shared test code."""

from __future__ import annotations

from pathlib import Path
from shutil import copy2

import pytest


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


@pytest.fixture(name="test_terminal_source")
def fixture_test_terminal_source() -> Path:
    return Path(__file__).parent / "test_data" / "terminal_source.json"


@pytest.fixture(name="test_terminal_target")
def fixture_test_terminal_target(tmp_path: Path) -> Path:
    test_file = Path(__file__).parent / "test_data" / "terminal_target.json"
    tmp_file = tmp_path / "settings.json"
    copy2(src=test_file, dst=tmp_file)
    return tmp_file


@pytest.fixture(name="test_home_dir", scope="class")
def fixture_test_home_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty tmp directory to use as the hwconfig home dir, monkeypatched to the HWCONFIG_HOME env var."""
    monkeypatch.setenv("HWCONFIG_ROOT_DIR", tmp_path.as_posix())
    return tmp_path
