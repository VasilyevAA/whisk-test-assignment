import os
import sys
import pytest


def run_test(file_name, capture_stdout=True, allure_dir=None):
    cmd = [
        file_name, "-vvv",
        # '-n', '3'
    ]

    if capture_stdout:
        cmd.append("-s")

    test_name = os.path.splitext(os.path.basename(file_name))[0]
    alluredir = os.path.normpath("%s/%s/" % (allure_dir or "allure-results", test_name))
    cmd.extend(["--alluredir", alluredir])
    print(cmd)
    sys.exit(pytest.main(cmd))
