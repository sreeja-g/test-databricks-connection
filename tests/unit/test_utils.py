from src.utils import (
    count_medications,
    fever_flag,
)


def test_count_medications():

    assert (
        count_medications(
            "aspirin|metformin"
        )
        == 2
    )

    assert (
        count_medications(
            "aspirin"
        )
        == 1
    )


def test_count_medications_handles_empty_values():

    assert (
        count_medications("none")
        == 0
    )

    assert (
        count_medications("")
        == 0
    )

    assert (
        count_medications(None)
        == 0
    )


def test_fever_flag():

    assert (
        fever_flag(101.0)
        == 1
    )

    assert (
        fever_flag(100.4)
        == 1
    )

    assert (
        fever_flag(98.6)
        == 0
    )