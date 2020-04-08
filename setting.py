import os

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

BASE_UI_TEST_URL = os.getenv("UI_TEST_URL", "https://dev.whisk.com")
BASE_API_TEST_URL = os.getenv("UI_TEST_URL", "https://graph-dev.whisk.com")

WHISK_CLIENT_ID = os.getenv("WHISK_CLIENT_ID", "WCqJWnpNatcf3LUCxZmq94pR30sj2OOdBbMoGO8NGrMgUMk6Ogl4EMvLqcykNuGf")
