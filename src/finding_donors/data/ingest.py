"""Data ingestion and target creation."""

from __future__ import annotations

from pathlib import Path

from loguru import logger
import pandas as pd


def load_dataset(path: Path) -> pd.DataFrame:
    """Load source CSV with lightweight normalization."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    df = pd.read_csv(path, skipinitialspace=True)
    df.columns = [column.strip() for column in df.columns]

    logger.info("Loaded dataset from {} with shape {}", path, df.shape)
    return df


def create_binary_target(
    df: pd.DataFrame,
    target_column: str,
    positive_label: str,
    output_column: str = "target",
) -> tuple[pd.DataFrame, float]:
    """Create binary target aligned with business objective."""
    frame = df.copy()
    frame[target_column] = frame[target_column].astype(str).str.strip()
    frame[output_column] = (frame[target_column] == positive_label).astype(int)

    positive_rate = float(frame[output_column].mean())
    logger.info("Positive class rate on source data: {:.2f}%", positive_rate * 100.0)
    return frame, positive_rate

