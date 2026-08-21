from pathlib import Path

import numpy as np
import pytest

from src.modeling import (
    predict,
    train_model,
)

from src.preprocessing import (
    load_data,
    prepare_xy,
)


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "ehr_sample.csv"
)


@pytest.mark.parametrize(
    "target",
    [
        "hospitalized_30d",
        "er_visit_30d",
    ],
)
def test_classification_models_train_and_predict(
    target,
):

    df = load_data(
        DATA_PATH
    )

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

    assert (
        len(predictions)
        == len(df)
    )

    assert set(
        predictions
    ).issubset(
        {0, 1}
    )


def test_los_model_trains_and_predicts_valid_values():

    df = load_data(
        DATA_PATH
    )

    target = (
        "length_of_stay_days"
    )

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

    assert (
        len(predictions)
        == len(df)
    )

    assert (
        np.isfinite(
            predictions
        )
        .all()
    )

    assert (
        predictions >= 0
    ).all()