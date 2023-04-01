import json
from pathlib import Path

import pytest

from hwconfig.install import copy_terminal_settings, get_sync_config_data_dir


@pytest.fixture(scope="function", name="setup_files")
def fixture_setup_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    """Test setup fixture, set hwconfig home to a tmp dir and create a dummy terminal
    settings file to write to during the test.

    Args:
        tmp_path: Pytest fixture providing a temp directory
        monkeypatch: Pytest fixture for monkeypatching attributes etc.

    Returns:
        A tuple with the path to the settings source and destination files.
    """
    monkeypatch.setenv("HWCONFIG_HOME", tmp_path.as_posix())
    config_data_dir = get_sync_config_data_dir()
    source_file = config_data_dir / "terminal" / "settings.json"
    test_data_file = Path(__file__).parent / "test_data" / "terminal_settings.json"

    with open(test_data_file, "r", encoding="utf-8") as f:
        destination_data = json.load(f)

    destination_file = tmp_path / "destination.json"

    with open(destination_file, "w", encoding="utf-8") as f:
        json.dump(destination_data, f)

    return source_file, destination_file


def test_copy_terminal_settings(setup_files: tuple[Path, Path]) -> None:
    """Check that the function copies profiles and default settings from the source

    Args:
        setup_files: Pytest setup fixture
    """
    source_file, destination_file = setup_files

    copy_terminal_settings(source_file, destination_file)

    with open(destination_file, encoding="utf-8") as f:
        destination_data = json.load(f)

    assert destination_data["profiles"]["defaults"]["colorScheme"] == "Dracula"
    assert destination_data["alwaysShowTabs"] is True


def test_copy_terminal_settings_schemes(setup_files: tuple[Path, Path]) -> None:
    """Check that the function copies themes from source

    Args:
        setup_files: Pytest setup fixture
    """
    source_file, destination_file = setup_files

    copy_terminal_settings(source_file, destination_file)

    with open(destination_file, encoding="utf-8") as f:
        destination_data = json.load(f)

    dracula_schemes = [x for x in destination_data["schemes"] if x["name"] == "Dracula"]
    monokai_pro_schemes = [
        x for x in destination_data["schemes"] if "Monokai Pro" in x["name"]
    ]

    assert len(dracula_schemes) == 1
    assert len(monokai_pro_schemes) == 3
