from pathlib import Path

import pandas as pd

from src.utils import (
    count_medications,
    fever_flag,
)


FEATURE_COLUMNS = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "temperature_f",
    "spo2",
    "respiratory_rate",
    "chronic_condition_count",
    "prior_er_visits_6m",
    "prior_hospitalizations_6m",
]


TARGET_COLUMNS = [
    "hospitalized_30d",
    "er_visit_30d",
    "length_of_stay_days",
]


REQUIRED_COLUMNS = [
    "patient_id",
    "medications",
    *FEATURE_COLUMNS,
    *TARGET_COLUMNS,
]


def load_data(
    path: str | Path,
) -> pd.DataFrame:

    df = pd.read_csv(path)

    validate_data(df)

    return df


def validate_data(
    df: pd.DataFrame,
) -> None:

    missing_columns = sorted(
        set(REQUIRED_COLUMNS)
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    if df["patient_id"].duplicated().any():
        raise ValueError(
            "patient_id must be unique"
        )

    for target in [
        "hospitalized_30d",
        "er_visit_30d",
    ]:

        values = set(
            df[target]
            .dropna()
            .unique()
        )

        if not values.issubset({0, 1}):
            raise ValueError(
                f"{target} must contain only 0/1"
            )

    if (
        df[TARGET_COLUMNS]
        .isna()
        .any()
        .any()
    ):
        raise ValueError(
            "Target columns cannot "
            "contain missing values"
        )

    if (
        df["length_of_stay_days"] < 0
    ).any():
        raise ValueError(
            "length_of_stay_days "
            "cannot be negative"
        )

    spo2 = df["spo2"].dropna()

    if (
        (spo2 < 50)
        | (spo2 > 100)
    ).any():
        raise ValueError(
            "spo2 must be between "
            "50 and 100"
        )

    systolic_bp = (
        df["systolic_bp"]
        .dropna()
    )

    if (
        systolic_bp <= 0
    ).any():
        raise ValueError(
            "systolic_bp must be "
            "greater than 0"
        )


def build_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    validate_data(df)

    X = df[
        FEATURE_COLUMNS
    ].copy()

    X["medication_count"] = (
        df["medications"]
        .apply(count_medications)
    )

    X["fever_flag"] = (
        df["temperature_f"]
        .apply(fever_flag)
    )

    X["shock_index"] = (
        X["heart_rate"]
        / X["systolic_bp"]
    )

    return X


def prepare_xy(
    df: pd.DataFrame,
    target: str,
):

    if target not in TARGET_COLUMNS:
        raise ValueError(
            f"Unknown target: {target}"
        )

    X = build_features(df)

    y = df[target].copy()

    return X, y