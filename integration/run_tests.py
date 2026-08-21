import os
import sys
from pathlib import Path

import pytest


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

print(f"Current working directory: {os.getcwd()}")
print(f"Script file: {__file__}")
print(f"Bundle root: {ROOT_DIR}")

print("Bundle root contents:")
for item in ROOT_DIR.iterdir():
    print(f" - {item}")

sys.path.insert(0, str(ROOT_DIR))


def main():
    test_dir = ROOT_DIR / "tests" / "integration"

    print(f"Integration test directory: {test_dir}")
    print(f"Exists: {test_dir.exists()}")

    if not test_dir.exists():
        raise FileNotFoundError(
            f"Integration test directory not found: {test_dir}"
        )

    exit_code = pytest.main([
        str(test_dir),
        "-v",
        "-s",
    ])

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()