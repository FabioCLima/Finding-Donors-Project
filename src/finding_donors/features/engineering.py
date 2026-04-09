"""Feature engineering routines derived from notebook findings."""

from __future__ import annotations

from loguru import logger
import numpy as np
import pandas as pd


def engineer_features(
    df: pd.DataFrame,
    rare_country_min_support: int,
) -> pd.DataFrame:
    """Apply deterministic feature transforms used in the ML pipeline."""
    frame = df.copy()

    numeric_source_cols = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
    for column in numeric_source_cols:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    if frame[numeric_source_cols].isna().any().any():
        null_summary = frame[numeric_source_cols].isna().sum()
        raise ValueError(
            "Numeric source columns have null values after coercion: "
            f"{null_summary[null_summary > 0].to_dict()}"
        )

    frame["capital_gain_flag"] = (frame["capital-gain"] > 0).astype(int)
    frame["capital_loss_flag"] = (frame["capital-loss"] > 0).astype(int)
    frame["capital_gain_log"] = np.log1p(frame["capital-gain"])
    frame["capital_loss_log"] = np.log1p(frame["capital-loss"])

    country_series = frame["native-country"].astype(str).str.strip()
    country_counts = country_series.value_counts()
    rare_countries = country_counts[country_counts < rare_country_min_support].index
    frame["native-country-grouped"] = country_series.where(
        ~country_series.isin(rare_countries), "Other"
    )
    logger.info("Grouped {} rare countries into 'Other'.", len(rare_countries))

    return frame

