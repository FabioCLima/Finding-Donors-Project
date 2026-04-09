"""Candidate model catalog."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


@dataclass(frozen=True)
class ModelSpec:
    """Catalog entry describing model family and estimator."""

    family: str
    estimator: object


def get_model_catalog(random_state: int) -> dict[str, ModelSpec]:
    """Return benchmark and candidate models."""
    return {
        "DummyMostFrequent": ModelSpec(
            family="benchmark",
            estimator=DummyClassifier(strategy="most_frequent"),
        ),
        "DummyAlwaysPositive": ModelSpec(
            family="benchmark",
            estimator=DummyClassifier(strategy="constant", constant=1),
        ),
        "LogisticRegression": ModelSpec(
            family="candidate",
            estimator=LogisticRegression(
                max_iter=2000,
                solver="liblinear",
                random_state=random_state,
            ),
        ),
        "LogisticRegressionBalanced": ModelSpec(
            family="candidate",
            estimator=LogisticRegression(
                max_iter=2000,
                solver="liblinear",
                class_weight="balanced",
                random_state=random_state,
            ),
        ),
        "RandomForest": ModelSpec(
            family="candidate",
            estimator=RandomForestClassifier(
                n_estimators=400,
                min_samples_leaf=2,
                min_samples_split=10,
                random_state=random_state,
                n_jobs=1,
            ),
        ),
        "HistGradientBoosting": ModelSpec(
            family="candidate",
            estimator=HistGradientBoostingClassifier(
                learning_rate=0.05,
                max_depth=6,
                max_iter=250,
                min_samples_leaf=20,
                random_state=random_state,
            ),
        ),
    }

