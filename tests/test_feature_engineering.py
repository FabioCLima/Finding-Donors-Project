import pandas as pd

from finding_donors.features.engineering import engineer_features


def test_engineer_features_creates_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "age": [39, 50],
            "education-num": [13, 13],
            "capital-gain": [2174.0, 0.0],
            "capital-loss": [0.0, 0.0],
            "hours-per-week": [40.0, 13.0],
            "native-country": ["United-States", "Canada"],
        }
    )
    transformed = engineer_features(df, rare_country_min_support=2)
    assert "capital_gain_flag" in transformed.columns
    assert "capital_loss_flag" in transformed.columns
    assert "capital_gain_log" in transformed.columns
    assert "capital_loss_log" in transformed.columns
    assert "native-country-grouped" in transformed.columns

