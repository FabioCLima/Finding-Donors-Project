"""Dataset split utilities."""

from __future__ import annotations

from loguru import logger
import pandas as pd
from sklearn.model_selection import train_test_split


def split_train_test(
    df: pd.DataFrame,
    feature_columns: list[str],
    target_column: str,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data using stratified sampling."""
    missing_features = sorted(set(feature_columns) - set(df.columns))
    if missing_features:
        raise ValueError(f"Missing features required for training: {missing_features}")

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' is not present in dataframe.")

    X = df[feature_columns].copy()
    y = df[target_column].astype(int).copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    logger.info("Train shape: {} | Test shape: {}", X_train.shape, X_test.shape)
    return X_train, X_test, y_train, y_test

