"""Centralized configuration for the Finding Donors ML workflow."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
import warnings

from pydantic import BaseModel, ConfigDict, Field, field_validator

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - runtime fallback
    yaml = None

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class RuntimeEnvironment(BaseModel):
    """Runtime overrides loaded from environment variables."""

    model_config = ConfigDict(extra="ignore")

    config_path: Path = Field(default=PROJECT_ROOT / "configs" / "base.yaml")
    log_level: str = "INFO"
    log_file: Path = Field(
        default=PROJECT_ROOT / "reports" / "experiments" / "pipeline.log"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        allowed = {
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }
        normalized = value.upper()
        if normalized not in allowed:
            raise ValueError(f"log_level must be one of {sorted(allowed)}")
        return normalized

    @classmethod
    def from_env(cls) -> "RuntimeEnvironment":
        """Create runtime settings using environment variable overrides."""
        return cls(
            config_path=Path(
                os.getenv("FD_CONFIG_PATH", str(PROJECT_ROOT / "configs" / "base.yaml"))
            ),
            log_level=os.getenv("FD_LOG_LEVEL", "INFO"),
            log_file=Path(
                os.getenv(
                    "FD_LOG_FILE",
                    str(PROJECT_ROOT / "reports" / "experiments" / "pipeline.log"),
                )
            ),
        )


class PathsConfig(BaseModel):
    """Paths used by the workflow."""

    model_config = ConfigDict(extra="forbid")

    raw_data: Path = Path("data/raw/census.csv")
    model_dir: Path = Path("models")
    figure_dir: Path = Path("figs")
    reports_dir: Path = Path("reports/metrics")
    experiments_dir: Path = Path("reports/experiments")
    processed_snapshot: Path = Path("data/processed/census_features.csv")


class RuntimeConfig(BaseModel):
    """Training runtime settings."""

    model_config = ConfigDict(extra="forbid")

    random_state: int = 42
    test_size: float = 0.2
    beta: float = 0.5
    cv_splits: int = 5
    threshold_candidates: list[float] = Field(
        default_factory=lambda: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    )

    @field_validator("test_size")
    @classmethod
    def validate_test_size(cls, value: float) -> float:
        if not 0.0 < value < 1.0:
            raise ValueError("test_size must be between 0 and 1")
        return value

    @field_validator("cv_splits")
    @classmethod
    def validate_cv_splits(cls, value: int) -> int:
        if value < 2:
            raise ValueError("cv_splits must be >= 2")
        return value


class DataConfig(BaseModel):
    """Data contract and business labels."""

    model_config = ConfigDict(extra="forbid")

    target_col: str = "income"
    binary_target_col: str = "target"
    positive_label: str = ">50K"
    rare_country_min_support: int = 50
    required_columns: list[str] = Field(
        default_factory=lambda: [
            "age",
            "workclass",
            "education_level",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
            "income",
        ]
    )
    numeric_source_columns: list[str] = Field(
        default_factory=lambda: [
            "age",
            "education-num",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
        ]
    )
    drop_columns: list[str] = Field(default_factory=lambda: ["education-num", "fnlwgt"])
    sensitive_columns: list[str] = Field(
        default_factory=lambda: ["sex", "race", "native-country"]
    )


class FeatureConfig(BaseModel):
    """Feature lists used by the model pipeline."""

    model_config = ConfigDict(extra="forbid")

    numeric_features: list[str] = Field(
        default_factory=lambda: [
            "age",
            "hours-per-week",
            "capital_gain_log",
            "capital_loss_log",
            "capital_gain_flag",
            "capital_loss_flag",
        ]
    )
    categorical_features: list[str] = Field(
        default_factory=lambda: [
            "workclass",
            "education_level",
            "marital-status",
            "occupation",
            "relationship",
        ]
    )


class ModelsConfig(BaseModel):
    """Modeling settings."""

    model_config = ConfigDict(extra="forbid")

    n_jobs: int = -1
    tune_iterations: dict[str, int] = Field(
        default_factory=lambda: {
            "HistGradientBoosting": 24,
            "RandomForest": 20,
            "LogisticRegression": 12,
            "LogisticRegressionBalanced": 12,
        }
    )


class ResolvedPaths(BaseModel):
    """Absolute resolved paths."""

    model_config = ConfigDict(extra="forbid")

    raw_data: Path
    model_dir: Path
    figure_dir: Path
    reports_dir: Path
    experiments_dir: Path
    processed_snapshot: Path


class ProjectConfig(BaseModel):
    """Top-level project configuration."""

    model_config = ConfigDict(extra="forbid")

    paths: PathsConfig = Field(default_factory=PathsConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    features: FeatureConfig = Field(default_factory=FeatureConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)

    def _resolve(self, value: Path) -> Path:
        return value if value.is_absolute() else PROJECT_ROOT / value

    def resolved_paths(self) -> ResolvedPaths:
        return ResolvedPaths(
            raw_data=self._resolve(self.paths.raw_data),
            model_dir=self._resolve(self.paths.model_dir),
            figure_dir=self._resolve(self.paths.figure_dir),
            reports_dir=self._resolve(self.paths.reports_dir),
            experiments_dir=self._resolve(self.paths.experiments_dir),
            processed_snapshot=self._resolve(self.paths.processed_snapshot),
        )


def load_project_config(config_path: Path) -> ProjectConfig:
    """Load and validate project config from YAML."""
    if yaml is None:
        warnings.warn(
            "PyYAML is not installed. Falling back to default in-code configuration.",
            RuntimeWarning,
            stacklevel=2,
        )
        return ProjectConfig()

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        payload: dict[str, Any] = yaml.safe_load(file) or {}

    return ProjectConfig.model_validate(payload)
