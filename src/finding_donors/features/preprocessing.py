"""Preprocessing pipeline builders."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


def build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    """Create a sklearn preprocessor for numeric and categorical data."""
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


def build_model_pipeline(
    estimator: object,
    preprocessor: ColumnTransformer,
) -> Pipeline:
    """Compose preprocessor + estimator in a single sklearn Pipeline."""
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", estimator),
        ]
    )

