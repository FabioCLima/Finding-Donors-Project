from pathlib import Path

from finding_donors.core.config import PROJECT_ROOT, ProjectConfig


def test_default_config_has_expected_paths() -> None:
    config = ProjectConfig()
    resolved = config.resolved_paths()
    assert resolved.raw_data == PROJECT_ROOT / Path("data/raw/census.csv")
    assert resolved.model_dir == PROJECT_ROOT / Path("models")

