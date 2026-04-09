"""End-to-end training pipeline for Finding Donors."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from loguru import logger

from finding_donors.core.config import (
    PROJECT_ROOT,
    RuntimeEnvironment,
    load_project_config,
)
from finding_donors.core.logging import configure_logging
from finding_donors.data.contracts import build_dataset_contract, validate_dataframe_contract
from finding_donors.data.ingest import create_binary_target, load_dataset
from finding_donors.data.split import split_train_test
from finding_donors.evaluation.reporting import evaluate_holdout, plot_confusion_matrix
from finding_donors.evaluation.threshold import compute_oof_scores, search_best_threshold
from finding_donors.features.engineering import engineer_features
from finding_donors.features.preprocessing import build_model_pipeline, build_preprocessor
from finding_donors.models.catalog import get_model_catalog
from finding_donors.models.persistence import save_json, save_model
from finding_donors.models.train import get_cv, run_cross_validation
from finding_donors.models.tuning import run_tuning


def _ensure_directories(paths: dict[str, Path], log_file: Path) -> None:
    for name in ["model_dir", "figure_dir", "reports_dir", "experiments_dir"]:
        paths[name].mkdir(parents=True, exist_ok=True)
    paths["processed_snapshot"].parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)


def _resolve_dataset_path(configured_path: Path) -> Path:
    if configured_path.exists():
        return configured_path

    fallback = PROJECT_ROOT / "data" / "census.csv"
    if fallback.exists():
        logger.warning(
            "Configured dataset path {} not found. Falling back to {}.",
            configured_path,
            fallback,
        )
        return fallback

    raise FileNotFoundError(
        f"Dataset not found in configured path ({configured_path}) "
        f"or fallback path ({fallback})."
    )


def run_training_pipeline(
    config_path: Path | None = None,
    log_level_override: str | None = None,
) -> dict[str, Any]:
    """Run full ML pipeline and persist artifacts."""
    env = RuntimeEnvironment.from_env()
    effective_config_path = config_path or env.config_path
    config = load_project_config(effective_config_path)
    resolved = config.resolved_paths()
    paths = {
        "raw_data": resolved.raw_data,
        "model_dir": resolved.model_dir,
        "figure_dir": resolved.figure_dir,
        "reports_dir": resolved.reports_dir,
        "experiments_dir": resolved.experiments_dir,
        "processed_snapshot": resolved.processed_snapshot,
    }

    log_level = (log_level_override or env.log_level).upper()
    configure_logging(level=log_level, log_file=env.log_file)
    _ensure_directories(paths=paths, log_file=env.log_file)
    logger.info("Pipeline started with config file: {}", effective_config_path)

    dataset_path = _resolve_dataset_path(paths["raw_data"])
    df = load_dataset(dataset_path)
    validate_dataframe_contract(df, build_dataset_contract(config.data))
    df, baseline_positive_rate = create_binary_target(
        df=df,
        target_column=config.data.target_col,
        positive_label=config.data.positive_label,
        output_column=config.data.binary_target_col,
    )

    feature_df = engineer_features(
        df=df,
        rare_country_min_support=config.data.rare_country_min_support,
    )
    feature_df.to_csv(paths["processed_snapshot"], index=False)
    logger.info("Saved processed snapshot to {}", paths["processed_snapshot"])

    feature_columns = config.features.numeric_features + config.features.categorical_features
    X_train, X_test, y_train, y_test = split_train_test(
        df=feature_df,
        feature_columns=feature_columns,
        target_column=config.data.binary_target_col,
        test_size=config.runtime.test_size,
        random_state=config.runtime.random_state,
    )

    preprocessor = build_preprocessor(
        numeric_features=config.features.numeric_features,
        categorical_features=config.features.categorical_features,
    )
    catalog = get_model_catalog(random_state=config.runtime.random_state)

    cv_summary, best_model_name, _trained_models = run_cross_validation(
        X_train=X_train,
        y_train=y_train,
        preprocessor=preprocessor,
        catalog=catalog,
        beta=config.runtime.beta,
        cv_splits=config.runtime.cv_splits,
        random_state=config.runtime.random_state,
        n_jobs=config.models.n_jobs,
    )
    cv_summary.to_csv(paths["reports_dir"] / "cv_summary.csv", index=False)
    logger.info("Cross-validation summary saved to reports.")

    best_pipeline_template = build_model_pipeline(
        estimator=deepcopy(catalog[best_model_name].estimator),
        preprocessor=deepcopy(preprocessor),
    )
    tuned_model, tuned_cv_score, tuned_params, tuning_results = run_tuning(
        pipeline_template=best_pipeline_template,
        model_name=best_model_name,
        X_train=X_train,
        y_train=y_train,
        beta=config.runtime.beta,
        cv_splits=config.runtime.cv_splits,
        random_state=config.runtime.random_state,
        n_iter=config.models.tune_iterations.get(best_model_name, 12),
        n_jobs=config.models.n_jobs,
    )
    tuning_results.to_csv(paths["reports_dir"] / "tuning_results.csv", index=False)

    default_eval = evaluate_holdout(
        estimator=tuned_model,
        X_test=X_test,
        y_test=y_test,
        threshold=0.5,
        beta=config.runtime.beta,
        label=f"{best_model_name} @0.50",
    )
    oof_scores = compute_oof_scores(
        estimator=tuned_model,
        X_train=X_train,
        y_train=y_train,
        cv=get_cv(
            cv_splits=config.runtime.cv_splits,
            random_state=config.runtime.random_state,
        ),
        n_jobs=config.models.n_jobs,
    )
    threshold_table, tuned_threshold = search_best_threshold(
        y_true=y_train,
        scores=oof_scores,
        beta=config.runtime.beta,
        fixed_candidates=config.runtime.threshold_candidates,
    )
    threshold_table.to_csv(paths["reports_dir"] / "threshold_table.csv", index=False)

    threshold_eval = evaluate_holdout(
        estimator=tuned_model,
        X_test=X_test,
        y_test=y_test,
        threshold=tuned_threshold,
        beta=config.runtime.beta,
        label=f"{best_model_name} @{tuned_threshold:.2f}",
    )

    final_eval = threshold_eval
    final_threshold = tuned_threshold
    if threshold_eval["metrics"]["f0_5"] < default_eval["metrics"]["f0_5"]:
        final_eval = default_eval
        final_threshold = 0.5

    model_path = paths["model_dir"] / "best_model.joblib"
    save_model(model=tuned_model, path=model_path)

    plot_confusion_matrix(
        confusion_matrix_values=final_eval["confusion_matrix"],
        output_path=paths["figure_dir"] / "confusion_matrix.png",
        title=f"Confusion Matrix - {best_model_name}",
    )
    with (paths["reports_dir"] / "classification_report.txt").open(
        "w", encoding="utf-8"
    ) as report_file:
        report_file.write(str(final_eval["classification_report"]))

    metadata = {
        "model_name": best_model_name,
        "baseline_positive_rate": baseline_positive_rate,
        "best_cv_score_f0_5": tuned_cv_score,
        "best_params": tuned_params,
        "final_threshold": final_threshold,
        "holdout_metrics": final_eval["metrics"],
        "feature_columns": feature_columns,
        "dataset_path": str(dataset_path),
        "config_path": str(effective_config_path),
    }
    save_json(metadata, paths["model_dir"] / "metadata.json")
    save_json(final_eval["metrics"], paths["reports_dir"] / "holdout_metrics.json")

    logger.info("Pipeline completed successfully. Model stored at {}", model_path)
    return {
        "model_path": model_path,
        "metadata_path": paths["model_dir"] / "metadata.json",
        "metrics_path": paths["reports_dir"] / "holdout_metrics.json",
    }
