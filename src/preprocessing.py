"""Preprocessamento: split estratificado e ColumnTransformer."""

import logging

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from src.config import (
    CORE_CATEGORICAL,
    CORE_NUMERIC,
    RANDOM_STATE,
    TEST_SIZE,
)

logger = logging.getLogger(__name__)


def split_data(df):
    """Separa features e target, faz train/test split estratificado."""
    target = df["target"].copy()
    feature_cols = CORE_NUMERIC + CORE_CATEGORICAL
    X = df[feature_cols].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )
    logger.info("Train: %s, Test: %s", X_train.shape, X_test.shape)
    return X_train, X_test, y_train, y_test


def build_preprocessor(numeric_features=None, categorical_features=None):
    """Constrói o ColumnTransformer com MinMaxScaler e OneHotEncoder."""
    if numeric_features is None:
        numeric_features = CORE_NUMERIC
    if categorical_features is None:
        categorical_features = CORE_CATEGORICAL

    return ColumnTransformer(
        transformers=[
            ("num", MinMaxScaler(), numeric_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
        ],
        remainder="drop",
    )


def make_modeling_pipeline(estimator, numeric_features=None, categorical_features=None):
    """Encapsula preprocessor + estimador em um Pipeline sklearn."""
    return Pipeline(
        steps=[
            (
                "preprocess",
                build_preprocessor(numeric_features, categorical_features),
            ),
            ("model", estimator),
        ]
    )
