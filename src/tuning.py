"""Otimização de hiperparâmetros do modelo campeão via RandomizedSearchCV."""

import logging

import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import RandomizedSearchCV

from src.config import RANDOM_STATE
from src.train import get_cv, get_scoring

logger = logging.getLogger(__name__)


def get_tuning_setup(model_name):
    """Retorna o espaço de busca adequado à família do modelo campeão."""
    if model_name == "HistGradientBoosting":
        return {
            "n_iter": 24,
            "param_distributions": {
                "model__learning_rate": [0.01, 0.03, 0.05, 0.07, 0.10, 0.15],
                "model__max_depth": [3, 4, 5, 6, 8, None],
                "model__max_iter": [100, 150, 200, 250, 350],
                "model__min_samples_leaf": [10, 20, 30, 50],
                "model__l2_regularization": [0.0, 0.01, 0.10, 1.0],
            },
        }

    if model_name == "RandomForest":
        return {
            "n_iter": 20,
            "param_distributions": {
                "model__n_estimators": [200, 300, 400, 600],
                "model__max_depth": [4, 6, 8, 12, None],
                "model__min_samples_leaf": [1, 2, 4, 8],
                "model__min_samples_split": [2, 5, 10, 20],
                "model__max_features": ["sqrt", "log2", None],
            },
        }

    # Fallback para modelos lineares
    return {
        "n_iter": 12,
        "param_distributions": {
            "model__C": [0.01, 0.05, 0.10, 0.50, 1.0, 2.0, 5.0, 10.0],
        },
    }


def run_tuning(pipeline, model_name, X_train, y_train):
    """Executa RandomizedSearchCV e retorna o melhor estimador."""
    setup = get_tuning_setup(model_name)
    scoring = get_scoring()
    cv = get_cv()

    logger.info(
        "Tuning %s com %d iterações ...", model_name, setup["n_iter"]
    )

    search = RandomizedSearchCV(
        estimator=clone(pipeline),
        param_distributions=setup["param_distributions"],
        n_iter=setup["n_iter"],
        scoring=scoring["f0_5"],
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
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

    logger.info("Melhor F0.5 (CV): %.4f", search.best_score_)
    logger.info("Melhores hiperparâmetros: %s", search.best_params_)

    return search.best_estimator_, search.best_score_, search.best_params_, results
