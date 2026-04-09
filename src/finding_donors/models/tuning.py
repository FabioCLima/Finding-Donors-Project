"""Hyperparameter tuning utilities."""

from __future__ import annotations

import pandas as pd
from loguru import logger
from sklearn.base import clone
from sklearn.model_selection import RandomizedSearchCV

from finding_donors.models.train import get_cv, get_scoring


def get_search_space(model_name: str) -> dict[str, list[object]]:
    """Return parameter search space per model family."""
    if model_name == "HistGradientBoosting":
        return {
            "model__learning_rate": [0.01, 0.03, 0.05, 0.07, 0.10, 0.15],
            "model__max_depth": [3, 4, 5, 6, 8, None],
            "model__max_iter": [100, 150, 200, 250, 350],
            "model__min_samples_leaf": [10, 20, 30, 50],
            "model__l2_regularization": [0.0, 0.01, 0.10, 1.0],
        }

    if model_name == "RandomForest":
        return {
            "model__n_estimators": [200, 300, 400, 600],
            "model__max_depth": [4, 6, 8, 12, None],
            "model__min_samples_leaf": [1, 2, 4, 8],
            "model__min_samples_split": [2, 5, 10, 20],
            "model__max_features": ["sqrt", "log2", None],
        }

    return {
        "model__C": [0.01, 0.05, 0.10, 0.50, 1.0, 2.0, 5.0, 10.0],
    }


def run_tuning(
    pipeline_template: object,
    model_name: str,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    beta: float,
    cv_splits: int,
    random_state: int,
    n_iter: int,
    n_jobs: int,
) -> tuple[object, float, dict[str, object], pd.DataFrame]:
    """Tune model with RandomizedSearchCV."""
    logger.info("Running RandomizedSearchCV for {} with {} iterations.", model_name, n_iter)
    search = RandomizedSearchCV(
        estimator=clone(pipeline_template),
        param_distributions=get_search_space(model_name),
        n_iter=n_iter,
        scoring=get_scoring(beta=beta)["f0_5"],
        cv=get_cv(cv_splits=cv_splits, random_state=random_state),
        random_state=random_state,
        n_jobs=n_jobs,
        refit=True,
        return_train_score=True,
        verbose=1,
    )
    search.fit(X_train, y_train)

    results = (
        pd.DataFrame(search.cv_results_)
        .sort_values(["rank_test_score", "mean_test_score"], ascending=[True, False])
        .reset_index(drop=True)
    )
    logger.info("Best tuned CV F0.5: {:.4f}", search.best_score_)
    logger.info("Best tuned params: {}", search.best_params_)

    return search.best_estimator_, float(search.best_score_), search.best_params_, results

