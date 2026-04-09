"""Metric calculation helpers."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    fbeta_score,
    precision_score,
    recall_score,
)


def compute_binary_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    beta: float,
) -> dict[str, float]:
    """Compute project-level binary metrics."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f0_5": float(fbeta_score(y_true, y_pred, beta=beta, zero_division=0)),
    }


def build_diagnostics(y_true: pd.Series, y_pred: pd.Series) -> tuple[object, str]:
    """Build confusion matrix and classification report."""
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(
        y_true,
        y_pred,
        target_names=["<=50K", ">50K"],
        zero_division=0,
    )
    return cm, report

