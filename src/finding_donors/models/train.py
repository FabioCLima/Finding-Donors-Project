"""Model training and cross-validation selection."""

from __future__ import annotations

from copy import deepcopy

from loguru import logger
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    fbeta_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

from finding_donors.features.preprocessing import build_model_pipeline
from finding_donors.models.catalog import ModelSpec


def get_scoring(beta: float) -> dict[str, object]:
    """Return the scoring dictionary used across model selection."""
    return {
        "f0_5": make_scorer(fbeta_score, beta=beta, zero_division=0),
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": make_scorer(recall_score, zero_division=0),
        "accuracy": make_scorer(accuracy_score),
    }


def get_cv(cv_splits: int, random_state: int) -> StratifiedKFold:
    """Build StratifiedKFold strategy."""
    return StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=random_state)


def _diagnose_generalization(
    family: str,
    val_f0_5_mean: float,
    generalization_gap_f0_5: float,
    best_dummy_f0_5: float,
) -> str:
    if family == "benchmark":
        return "benchmark"
    if val_f0_5_mean <= best_dummy_f0_5 + 0.03:
        return "underfitting"
    if generalization_gap_f0_5 >= 0.10:
        return "overfitting_strong"
    if generalization_gap_f0_5 >= 0.05:
        return "overfitting_moderate"
    return "stable_generalization"


def run_cross_validation(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
    catalog: dict[str, ModelSpec],
    beta: float,
    cv_splits: int,
    random_state: int,
    n_jobs: int,
) -> tuple[pd.DataFrame, str, dict[str, object]]:
    """Run CV for each model and return ranking + trained pipelines."""
    scoring = get_scoring(beta=beta)
    cv = get_cv(cv_splits=cv_splits, random_state=random_state)
    summary_rows: list[dict[str, object]] = []
    trained_pipelines: dict[str, object] = {}

    for model_name, spec in catalog.items():
        logger.info("Cross-validating model: {}", model_name)
        pipeline = build_model_pipeline(
            estimator=clone(spec.estimator),
            preprocessor=deepcopy(preprocessor),
        )

        cv_output = cross_validate(
            estimator=pipeline,
            X=X_train,
            y=y_train,
            cv=cv,
            scoring=scoring,
            return_train_score=True,
            n_jobs=n_jobs,
            error_score="raise",
        )

        train_f = float(np.mean(cv_output["train_f0_5"]))
        val_f = float(np.mean(cv_output["test_f0_5"]))

        summary_rows.append(
            {
                "model_name": model_name,
                "family": spec.family,
                "fit_time_mean": float(np.mean(cv_output["fit_time"])),
                "train_f0_5_mean": train_f,
                "val_f0_5_mean": val_f,
                "generalization_gap_f0_5": train_f - val_f,
                "val_precision_mean": float(np.mean(cv_output["test_precision"])),
                "val_recall_mean": float(np.mean(cv_output["test_recall"])),
                "val_accuracy_mean": float(np.mean(cv_output["test_accuracy"])),
            }
        )

        trained_pipelines[model_name] = clone(pipeline).fit(X_train, y_train)

    summary = pd.DataFrame(summary_rows)
    best_dummy_f0_5 = float(
        summary.loc[summary["family"] == "benchmark", "val_f0_5_mean"].max()
    )
    summary["diagnosis"] = summary.apply(
        lambda row: _diagnose_generalization(
            family=str(row["family"]),
            val_f0_5_mean=float(row["val_f0_5_mean"]),
            generalization_gap_f0_5=float(row["generalization_gap_f0_5"]),
            best_dummy_f0_5=best_dummy_f0_5,
        ),
        axis=1,
    )

    candidates = summary.loc[summary["family"] == "candidate"].sort_values(
        by=["val_f0_5_mean", "val_precision_mean", "generalization_gap_f0_5"],
        ascending=[False, False, True],
    )
    best_model_name = str(candidates.iloc[0]["model_name"])
    logger.info("Best candidate selected by CV: {}", best_model_name)

    return summary, best_model_name, trained_pipelines

