import sys
from pathlib import Path

import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.modeling import (
    predict,
    train_model,
)

from src.preprocessing import (
    load_data,
    prepare_xy,
)


DATA_PATH = (
    ROOT_DIR
    / "data"
    / "ehr_sample.csv"
)


def test_classification_target(df, target):
    print(f"Testing {target}")

    model = train_model(
        df,
        target,
    )

    X, _ = prepare_xy(
        df,
        target,
    )

    predictions = predict(
        model,
        X,
        target,
    )

    assert len(predictions) == len(df)

    assert set(
        predictions
    ).issubset({0, 1})

    print(
        f"{target}: PASS"
    )


def test_length_of_stay(df):
    target = "length_of_stay_days"

    print(f"Testing {target}")

    model = train_model(
        df,
        target,
    )

    X, _ = prepare_xy(
        df,
        target,
    )

    predictions = predict(
        model,
        X,
        target,
    )

    assert len(predictions) == len(df)

    assert np.isfinite(
        predictions
    ).all()

    assert (
        predictions >= 0
    ).all()

    print(
        f"{target}: PASS"
    )


def main():
    print(
        "Starting Databricks integration tests"
    )

    # Test that bundled data can actually be found
    assert DATA_PATH.exists(), (
        f"Dataset not found: {DATA_PATH}"
    )

    df = load_data(DATA_PATH)

    # Test that the deployed dataset loaded
    assert len(df) > 0

    # Test actual deployed ML pipeline
    test_classification_target(
        df,
        "hospitalized_30d",
    )

    test_classification_target(
        df,
        "er_visit_30d",
    )

    test_length_of_stay(df)

    print(
        "ALL DATABRICKS INTEGRATION TESTS PASSED"
    )


if __name__ == "__main__":
    main()