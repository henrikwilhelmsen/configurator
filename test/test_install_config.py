import json
from pathlib import Path

import pytest

from hwconfig.install import copy_terminal_settings, HWCONFIG_DIR


@pytest.fixture(scope="function", name="setup_files")
def fixture_setup_files(tmp_path: Path) -> tuple[Path, Path]:
    source_file = HWCONFIG_DIR / "terminal" / "settings.json"
    test_data_file = Path(__file__).parent / "test_data" / "terminal_settings.json"

    with open(test_data_file, "r", encoding="utf-8") as f:
        destination_data = json.load(f)

    destination_file = tmp_path / "destination.json"

    with open(destination_file, "w", encoding="utf-8") as f:
        json.dump(destination_data, f)

    return source_file, destination_file


def test_copy_terminal_settings(setup_files: tuple[Path, Path]) -> None:
    source_file, destination_file = setup_files

    copy_terminal_settings(source_file, destination_file)

    with open(destination_file, encoding="utf-8") as f:
        destination_data = json.load(f)

    assert destination_data["profiles"]["defaults"]["colorScheme"] == "Dracula"
    assert destination_data["alwaysShowTabs"] is True


def test_copy_terminal_settings_schemes(setup_files: tuple[Path, Path]) -> None:
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
