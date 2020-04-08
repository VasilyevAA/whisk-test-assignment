from setting import BASE_UI_TEST_URL
from splinter.driver import DriverAPI


class PageObjectQA:
    URL = ''

    def __init__(self, splinter_browser: DriverAPI = None, should_try_url_open=False):
        self.browser = splinter_browser or None  # or none because i think splinter implement singleton browser
        self.page_url = BASE_UI_TEST_URL + self.URL
        if should_try_url_open:
            self.browser.visit(self.page_url)
