"""Holdout evaluation and charting."""

from __future__ import annotations

import os
from pathlib import Path

from loguru import logger
import pandas as pd

from finding_donors.evaluation.metrics import build_diagnostics, compute_binary_metrics
from finding_donors.evaluation.threshold import get_positive_scores


def evaluate_holdout(
    estimator: object,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float,
    beta: float,
    label: str,
) -> dict[str, object]:
    """Evaluate a model on the holdout set with a chosen threshold."""
    scores = get_positive_scores(estimator=estimator, X=X_test)
    y_pred = (scores >= threshold).astype(int)

    metrics = compute_binary_metrics(y_true=y_test, y_pred=y_pred, beta=beta)
    metrics["threshold"] = float(threshold)
    metrics["model_name"] = label
    confusion, report = build_diagnostics(y_true=y_test, y_pred=y_pred)

    logger.info(
        "Holdout {} -> F0.5={:.4f} | precision={:.4f} | recall={:.4f} | accuracy={:.4f}",
        label,
        metrics["f0_5"],
        metrics["precision"],
        metrics["recall"],
        metrics["accuracy"],
    )

    return {
        "metrics": metrics,
        "confusion_matrix": confusion,
        "classification_report": report,
        "predictions": y_pred,
    }


def plot_confusion_matrix(confusion_matrix_values: object, output_path: Path, title: str) -> None:
    """Generate confusion matrix figure using seaborn."""
    os.environ.setdefault("MPLCONFIGDIR", str(output_path.parent.resolve()))
    import matplotlib.pyplot as plt
    import seaborn as sns

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        confusion_matrix_values,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Pred <=50K", "Pred >50K"],
        yticklabels=["True <=50K", "True >50K"],
    )
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
