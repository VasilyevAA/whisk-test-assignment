import sys
import pytest
from pathlib import Path


def run_test(file_name, capture_stdout=True, allure_dir=None):
    cmd = [
        file_name, "-vvv",
    ]

    if capture_stdout:
        cmd.append("-s")

    full_path = Path(file_name).resolve()
    allure_dir = Path(f"{allure_dir or 'allure-results'}/{full_path.stem}/").resolve()
    cmd.extend(["--alluredir", str(allure_dir)])
    print(cmd)
    sys.exit(pytest.main(cmd))
