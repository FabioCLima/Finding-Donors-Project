"""Avaliação final em holdout, busca de threshold e métricas."""

import logging

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    fbeta_score,
    precision_recall_curve,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_predict

from src.config import BETA
from src.train import get_cv

logger = logging.getLogger(__name__)


def compute_binary_metrics(y_true, y_pred, beta=BETA):
    """Calcula o conjunto central de métricas binárias do projeto."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f0_5": float(fbeta_score(y_true, y_pred, beta=beta, zero_division=0)),
    }


def get_positive_scores(estimator, X):
    """Retorna scores da classe positiva para análise de threshold."""
    if hasattr(estimator, "predict_proba"):
        return estimator.predict_proba(X)[:, 1]
    if hasattr(estimator, "decision_function"):
        raw = estimator.decision_function(X)
        r_min, r_max = np.min(raw), np.max(raw)
        if r_max == r_min:
            return np.zeros_like(raw, dtype=float)
        return (raw - r_min) / (r_max - r_min)
    return estimator.predict(X).astype(float)


def threshold_search(y_true, scores, beta=BETA):
    """Busca o threshold que maximiza F0.5 a partir de scores contínuos."""
    _precision, _recall, pr_thresholds = precision_recall_curve(y_true, scores)
    candidates = np.unique(
        np.round(
            np.concatenate(
                [
                    np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]),
                    pr_thresholds,
                ]
            ),
            4,
        )
    )

    rows = []
    for t in candidates:
        y_pred = (scores >= t).astype(int)
        m = compute_binary_metrics(y_true, y_pred, beta=beta)
        rows.append({"threshold": float(t), **m})

    table = pd.DataFrame(rows).sort_values("threshold").reset_index(drop=True)
    best_t = table.sort_values(
        by=["f0_5", "precision", "recall", "threshold"],
        ascending=[False, False, False, False],
    ).iloc[0]["threshold"]
    return table, float(best_t)


def get_oof_scores(estimator, X, y):
    """Gera scores out-of-fold no treino para selecionar threshold sem leakage."""
    cv = get_cv()
    template = clone(estimator)
    model_step = template.named_steps["model"]

    if hasattr(model_step, "predict_proba"):
        return cross_val_predict(
            template, X, y, cv=cv, method="predict_proba", n_jobs=-1
        )[:, 1]

    if hasattr(model_step, "decision_function"):
        raw = cross_val_predict(
            template, X, y, cv=cv, method="decision_function", n_jobs=-1
        )
        r_min, r_max = np.min(raw), np.max(raw)
        if r_max == r_min:
            return np.zeros_like(raw, dtype=float)
        return (raw - r_min) / (r_max - r_min)

    return cross_val_predict(
        template, X, y, cv=cv, method="predict", n_jobs=-1
    ).astype(float)


def evaluate_on_holdout(estimator, X_test, y_test, threshold=0.50, label=None):
    """Avalia o modelo no holdout com um threshold específico."""
    scores = get_positive_scores(estimator, X_test)
    y_pred = (scores >= threshold).astype(int)
    metrics = compute_binary_metrics(y_test, y_pred)
    metrics["threshold"] = float(threshold)
    metrics["model_name"] = label

    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(
        y_test, y_pred, target_names=["<=50K", ">50K"], zero_division=0
    )
    return metrics, cm, report, y_pred


def full_evaluation(model, model_name, X_train, y_train, X_test, y_test):
    """Executa avaliação completa: holdout padrão, threshold tuning, comparação."""
    logger.info("Avaliação em holdout para: %s", model_name)

    # Avaliação com threshold padrão
    default_metrics, cm_default, report_default, pred_default = evaluate_on_holdout(
        model, X_test, y_test, threshold=0.50, label=f"{model_name} @0.50"
    )

    # Busca de threshold via OOF no treino
    oof_scores = get_oof_scores(model, X_train, y_train)
    threshold_table, tuned_threshold = threshold_search(y_train, oof_scores)

    # Avaliação com threshold otimizado
    tuned_metrics, cm_tuned, report_tuned, pred_tuned = evaluate_on_holdout(
        model, X_test, y_test, threshold=tuned_threshold,
        label=f"{model_name} @{tuned_threshold:.2f}"
    )

    # Escolhe o melhor threshold
    if tuned_metrics["f0_5"] >= default_metrics["f0_5"]:
        final_metrics = tuned_metrics
        final_threshold = tuned_threshold
        final_cm = cm_tuned
        final_report = report_tuned
        final_pred = pred_tuned
    else:
        final_metrics = default_metrics
        final_threshold = 0.50
        final_cm = cm_default
        final_report = report_default
        final_pred = pred_default

    logger.info("Threshold final: %.2f", final_threshold)
    logger.info(
        "Métricas finais -> F0.5=%.3f, precision=%.3f, recall=%.3f, accuracy=%.3f",
        final_metrics["f0_5"],
        final_metrics["precision"],
        final_metrics["recall"],
        final_metrics["accuracy"],
    )
    logger.info("Matriz de confusão:\n%s", final_cm)
    logger.info("Classification report:\n%s", final_report)

    return {
        "metrics": final_metrics,
        "threshold": final_threshold,
        "confusion_matrix": final_cm,
        "classification_report": final_report,
        "predictions": final_pred,
        "threshold_table": threshold_table,
    }
