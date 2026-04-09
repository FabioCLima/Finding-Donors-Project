"""Dataset contract validation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from loguru import logger
import pandas as pd

from finding_donors.core.config import DataConfig


class DatasetContract(BaseModel):
    """Structural expectations for the source dataset."""

    model_config = ConfigDict(extra="forbid")

    required_columns: tuple[str, ...]
    numeric_columns: tuple[str, ...]
    target_column: str


def build_dataset_contract(data_config: DataConfig) -> DatasetContract:
    """Create the dataset contract from application config."""
    return DatasetContract(
        required_columns=tuple(data_config.required_columns),
        numeric_columns=tuple(data_config.numeric_source_columns),
        target_column=data_config.target_col,
    )


def validate_dataframe_contract(df: pd.DataFrame, contract: DatasetContract) -> None:
    """Validate required columns and numeric coercion."""
    missing_columns = sorted(set(contract.required_columns) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column in contract.numeric_columns:
        coerced = pd.to_numeric(df[column], errors="coerce")
        null_count = int(coerced.isna().sum())
        if null_count > 0:
            raise ValueError(
                f"Column '{column}' has {null_count} non-numeric values after coercion."
            )

    if df[contract.target_column].isna().any():
        raise ValueError(f"Target column '{contract.target_column}' contains null values.")

    logger.info("Dataset contract validation completed successfully.")

