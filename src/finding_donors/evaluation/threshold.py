"""Threshold search utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import precision_recall_curve

from finding_donors.evaluation.metrics import compute_binary_metrics


def get_positive_scores(estimator: object, X: pd.DataFrame) -> np.ndarray:
    """Return positive class scores for threshold tuning."""
    if hasattr(estimator, "predict_proba"):
        return estimator.predict_proba(X)[:, 1]

    if hasattr(estimator, "decision_function"):
        raw = estimator.decision_function(X)
        minimum = np.min(raw)
        maximum = np.max(raw)
        if maximum == minimum:
            return np.zeros_like(raw, dtype=float)
        return (raw - minimum) / (maximum - minimum)

    return estimator.predict(X).astype(float)


def search_best_threshold(
    y_true: pd.Series,
    scores: np.ndarray,
    beta: float,
    fixed_candidates: list[float],
) -> tuple[pd.DataFrame, float]:
    """Search threshold maximizing F0.5 score."""
    _precision, _recall, pr_thresholds = precision_recall_curve(y_true, scores)
    candidates = np.unique(
        np.round(
            np.concatenate([np.array(fixed_candidates), pr_thresholds]),
            4,
        )
    )

    rows: list[dict[str, float]] = []
    for threshold in candidates:
        y_pred = (scores >= threshold).astype(int)
        metrics = compute_binary_metrics(y_true=y_true, y_pred=y_pred, beta=beta)
        rows.append({"threshold": float(threshold), **metrics})

    table = pd.DataFrame(rows).sort_values("threshold").reset_index(drop=True)
    best_threshold = float(
        table.sort_values(
            by=["f0_5", "precision", "recall", "threshold"],
            ascending=[False, False, False, False],
        ).iloc[0]["threshold"]
    )
    return table, best_threshold


def compute_oof_scores(
    estimator: object,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cv: StratifiedKFold,
    n_jobs: int,
) -> np.ndarray:
    """Compute out-of-fold scores to tune threshold without leakage."""
    model = clone(estimator)
    model_step = model.named_steps["model"]

    if hasattr(model_step, "predict_proba"):
        return cross_val_predict(
            model, X_train, y_train, cv=cv, method="predict_proba", n_jobs=n_jobs
        )[:, 1]

    if hasattr(model_step, "decision_function"):
        raw = cross_val_predict(
            model, X_train, y_train, cv=cv, method="decision_function", n_jobs=n_jobs
        )
        minimum = np.min(raw)
        maximum = np.max(raw)
        if maximum == minimum:
            return np.zeros_like(raw, dtype=float)
        return (raw - minimum) / (maximum - minimum)

    return cross_val_predict(
        model, X_train, y_train, cv=cv, method="predict", n_jobs=n_jobs
    ).astype(float)

