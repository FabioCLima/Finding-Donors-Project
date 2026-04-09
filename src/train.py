"""Catálogo de modelos, cross-validation e seleção do campeão."""

import logging

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    fbeta_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

from src.config import BETA, CV_SPLITS, RANDOM_STATE
from src.preprocessing import make_modeling_pipeline

logger = logging.getLogger(__name__)


def get_scoring():
    """Retorna o dicionário de métricas para cross_validate."""
    return {
        "f0_5": make_scorer(fbeta_score, beta=BETA, zero_division=0),
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": make_scorer(recall_score, zero_division=0),
        "accuracy": make_scorer(accuracy_score),
    }


def get_cv():
    """Retorna a estratégia de validação cruzada."""
    return StratifiedKFold(
        n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE
    )


def get_model_catalog():
    """Retorna o catálogo completo de modelos candidatos e benchmarks."""
    return {
        "DummyMostFrequent": {
            "family": "benchmark",
            "pipeline": make_modeling_pipeline(
                DummyClassifier(strategy="most_frequent")
            ),
        },
        "DummyAlwaysPositive": {
            "family": "benchmark",
            "pipeline": make_modeling_pipeline(
                DummyClassifier(strategy="constant", constant=1)
            ),
        },
        "LogisticRegression": {
            "family": "candidate",
            "pipeline": make_modeling_pipeline(
                LogisticRegression(
                    max_iter=2000, solver="liblinear", random_state=RANDOM_STATE
                )
            ),
        },
        "LogisticRegressionBalanced": {
            "family": "candidate",
            "pipeline": make_modeling_pipeline(
                LogisticRegression(
                    max_iter=2000,
                    solver="liblinear",
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                )
            ),
        },
        "RandomForest": {
            "family": "candidate",
            "pipeline": make_modeling_pipeline(
                RandomForestClassifier(
                    n_estimators=400,
                    min_samples_leaf=2,
                    min_samples_split=10,
                    random_state=RANDOM_STATE,
                    n_jobs=1,
                )
            ),
        },
        "HistGradientBoosting": {
            "family": "candidate",
            "pipeline": make_modeling_pipeline(
                HistGradientBoostingClassifier(
                    learning_rate=0.05,
                    max_depth=6,
                    max_iter=250,
                    min_samples_leaf=20,
                    random_state=RANDOM_STATE,
                )
            ),
        },
    }


def _diagnose_generalization(row, best_dummy_f0_5):
    """Diagnóstico heurístico de generalização."""
    if row["family"] == "benchmark":
        return "benchmark"
    if row["val_f0_5_mean"] <= best_dummy_f0_5 + 0.03:
        return "underfitting"
    if row["generalization_gap_f0_5"] >= 0.10:
        return "overfitting forte"
    if row["generalization_gap_f0_5"] >= 0.05:
        return "overfitting moderado"
    return "generalizacao estavel"


def run_cross_validation(X_train, y_train):
    """Executa CV para todos os modelos e retorna summary + pipelines treinados."""
    catalog = get_model_catalog()
    scoring = get_scoring()
    cv = get_cv()

    summary_rows = []

    for model_name, spec in catalog.items():
        logger.info("CV: %s ...", model_name)
        cv_output = cross_validate(
            estimator=spec["pipeline"],
            X=X_train,
            y=y_train,
            cv=cv,
            scoring=scoring,
            return_train_score=True,
            n_jobs=-1,
            error_score="raise",
        )

        train_f0_5_mean = float(np.mean(cv_output["train_f0_5"]))
        val_f0_5_mean = float(np.mean(cv_output["test_f0_5"]))

        summary_rows.append(
            {
                "model_name": model_name,
                "family": spec["family"],
                "fit_time_mean": float(np.mean(cv_output["fit_time"])),
                "train_f0_5_mean": train_f0_5_mean,
                "val_f0_5_mean": val_f0_5_mean,
                "generalization_gap_f0_5": train_f0_5_mean - val_f0_5_mean,
                "val_precision_mean": float(np.mean(cv_output["test_precision"])),
                "val_recall_mean": float(np.mean(cv_output["test_recall"])),
                "val_accuracy_mean": float(np.mean(cv_output["test_accuracy"])),
            }
        )

    summary = pd.DataFrame(summary_rows)

    best_dummy_f0_5 = summary.loc[
        summary["family"] == "benchmark", "val_f0_5_mean"
    ].max()

    summary["diagnosis"] = summary.apply(
        _diagnose_generalization, axis=1, best_dummy_f0_5=best_dummy_f0_5
    )

    # Seleciona o melhor candidato
    candidates = summary.loc[summary["family"] == "candidate"].sort_values(
        by=["val_f0_5_mean", "val_precision_mean", "generalization_gap_f0_5"],
        ascending=[False, False, True],
    )
    best_model_name = candidates.iloc[0]["model_name"]

    # Treina todos os modelos no treino completo
    trained_pipelines = {}
    for model_name, spec in catalog.items():
        trained_pipelines[model_name] = clone(spec["pipeline"]).fit(X_train, y_train)

    logger.info("Modelo campeão: %s", best_model_name)
    return summary, best_model_name, trained_pipelines, catalog
