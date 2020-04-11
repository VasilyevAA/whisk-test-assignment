import json
import os
from pathlib import Path

WHISK_CLIENT_ID = os.getenv("WHISK_CLIENT_ID", "")
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

BASE_UI_TEST_URL = os.getenv("UI_TEST_URL", "https://dev.whisk.com")
BASE_API_TEST_URL = os.getenv("UI_TEST_URL", "https://graph-dev.whisk.com")

WEB_DRIVER_NAME = os.getenv('WEB_DRIVER_NAME', 'firefox')  # remote, firefox, chrome


def get_test_browser_configs():
    browser_cfgs = json.loads((Path(__file__) / "../browser_config.json").resolve().read_text())
    return [dict({
        'name': 'Test assignment VAA',
        'browserstack.debug': True,
        # 'browserstack.console': 'errors',
        # 'browserstack.networkLog': True
    }, **i) for i in browser_cfgs]
