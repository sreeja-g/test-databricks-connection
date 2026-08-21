import sys

from pathlib import Path


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR),
    )


import pytest


def main() -> None:

    test_dir = (
        ROOT_DIR
        / "tests"
        / "integration"
    )

    print(
        "Running Databricks "
        "integration tests from:"
    )

    print(test_dir)

    exit_code = pytest.main(
        [
            str(test_dir),
            "-v",
        ]
    )

    raise SystemExit(
        exit_code
    )


if __name__ == "__main__":
    main()