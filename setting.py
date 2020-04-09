import json
import os
from pathlib import Path

WHISK_CLIENT_ID = os.getenv("WHISK_CLIENT_ID", "")
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

BASE_UI_TEST_URL = os.getenv("UI_TEST_URL", "https://dev.whisk.com")
BASE_API_TEST_URL = os.getenv("UI_TEST_URL", "https://graph-dev.whisk.com")

WEB_DRIVER_NAME = os.getenv('WEB_DRIVER_NAME', 'firefox')  # remote, firefox, chrome


def get_desired_capabilities():
    browser_cfg = (Path(__file__) / "../browser_config.json").resolve().read_text()
    return json.loads(browser_cfg)
