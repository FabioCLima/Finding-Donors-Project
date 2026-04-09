"""Orquestrador do pipeline completo de ML — Finding Donors."""

import json
import logging

import joblib

from src.config import CORE_CATEGORICAL, CORE_NUMERIC, MODELS_DIR
from src.data_loader import create_target, load_census
from src.evaluate import full_evaluation
from src.features import engineer_features
from src.preprocessing import split_data
from src.train import run_cross_validation
from src.tuning import run_tuning

logger = logging.getLogger(__name__)


def run_pipeline():
    """Executa o pipeline completo: dados → features → treino → tuning → avaliação → salvar."""

    # --- 1. Leitura dos dados ---
    logger.info("=" * 60)
    logger.info("ETAPA 1: Leitura dos dados")
    df = load_census()
    df, baseline = create_target(df)

    # --- 2. Feature engineering ---
    logger.info("=" * 60)
    logger.info("ETAPA 2: Feature engineering")
    df = engineer_features(df)

    # --- 3. Split e preprocessamento ---
    logger.info("=" * 60)
    logger.info("ETAPA 3: Split estratificado")
    X_train, X_test, y_train, y_test = split_data(df)

    # --- 4. Cross-validation e seleção ---
    logger.info("=" * 60)
    logger.info("ETAPA 4: Cross-validation e seleção do campeão")
    summary, best_model_name, trained_pipelines, catalog = run_cross_validation(
        X_train, y_train
    )
    logger.info("Resumo CV:\n%s", summary.to_string(index=False))

    # --- 5. Tuning do campeão ---
    logger.info("=" * 60)
    logger.info("ETAPA 5: Tuning de hiperparâmetros (%s)", best_model_name)
    best_pipeline = trained_pipelines[best_model_name]
    tuned_model, best_score, best_params, tuning_results = run_tuning(
        catalog[best_model_name]["pipeline"],
        best_model_name,
        X_train,
        y_train,
    )

    # --- 6. Avaliação final ---
    logger.info("=" * 60)
    logger.info("ETAPA 6: Avaliação final em holdout")
    eval_results = full_evaluation(
        tuned_model,
        f"{best_model_name} tuned",
        X_train,
        y_train,
        X_test,
        y_test,
    )

    # --- 7. Salvar artefatos ---
    logger.info("=" * 60)
    logger.info("ETAPA 7: Salvando artefatos em %s", MODELS_DIR)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(tuned_model, MODELS_DIR / "best_model.joblib")
    logger.info("Modelo salvo: best_model.joblib")

    metadata = {
        "model_name": best_model_name,
        "best_params": {k: _serialize(v) for k, v in best_params.items()},
        "best_cv_score_f0_5": float(best_score),
        "threshold": eval_results["threshold"],
        "holdout_metrics": eval_results["metrics"],
        "baseline_positive_rate": float(baseline),
        "features": {
            "numeric": CORE_NUMERIC,
            "categorical": CORE_CATEGORICAL,
        },
    }
    with open(MODELS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    logger.info("Metadados salvos: metadata.json")

    logger.info("=" * 60)
    logger.info("Pipeline concluído com sucesso!")
    return tuned_model, eval_results, metadata


def _serialize(value):
    """Converte valores para tipos serializáveis em JSON."""
    if value is None:
        return None
    if isinstance(value, (int, float, str, bool)):
        return value
    return str(value)