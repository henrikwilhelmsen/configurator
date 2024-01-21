"""Shared test code."""

from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import pytest


@pytest.fixture(name="class_monkeypatch", scope="class")
def class_fixture_monkeypatch() -> pytest.MonkeyPatch:
    """Class scoped monkeypatch fixture."""
    return pytest.MonkeyPatch()


@pytest.fixture(name="test_source_dir", scope="class")
def fixture_test_source_dir() -> Path:
    """Fixture containing the path to the test data directory.."""
    return Path(__file__).parent / "test_data" / "copy_dir"


@pytest.fixture(name="tmp_path_class", scope="class")
def fixture_tmp_path_class(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path, None, None]:
    """Class scoped tmp_path fixture."""
    tmp_dir = tmp_path_factory.mktemp(basename="tmp", numbered=True)
    yield tmp_dir
    rmtree(tmp_dir)


@pytest.fixture(name="test_target_dir", scope="class")
def fixture_test_target_dir(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path, None, None]:
    """A tmp directory to use as the target for installer tests."""
    tmp_dir = tmp_path_factory.mktemp(basename="tmp", numbered=True)
    tmp_file = tmp_dir.joinpath("hello.json")
    tmp_file.touch()

    yield tmp_dir

    rmtree(tmp_dir)


@pytest.fixture(name="test_home_dir", scope="class")
def fixture_test_home_dir(
    tmp_path_factory: pytest.TempPathFactory,
    class_monkeypatch: pytest.MonkeyPatch,
) -> Generator[Path, None, None]:
    """An empty tmp directory to use as the hwconfig home dir, monkeypatched to the HWCONFIG_HOME env var."""
    tmp_dir = tmp_path_factory.mktemp(basename="tmp", numbered=True)
    class_monkeypatch.setenv("HWCONFIG_HOME", tmp_dir.as_posix())
    yield tmp_dir
    rmtree(tmp_dir)
