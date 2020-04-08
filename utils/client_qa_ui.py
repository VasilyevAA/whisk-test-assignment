from splinter.driver.webdriver import WebDriverElement

from setting import BASE_UI_TEST_URL
from splinter.driver import DriverAPI


class WebElementObjQA:
    TESTID_CSS_TEMPLATE = '[data-testid = "%s"]'

    def find_by_testid(self, testid_data):
        return self.root_form.find_by_css(self.TESTID_CSS_TEMPLATE % testid_data)

    def __init__(self, form_element: WebDriverElement):
        self.root_form = form_element


class PageObjectQA:
    URL = ''
    TESTID_CSS_TEMPLATE = "[data-testid='%s']"

    def find_by_testid(self, testid_data, prefix='', suffix=''):
        css_selector = prefix + self.TESTID_CSS_TEMPLATE % testid_data + suffix
        print(css_selector)
        return self.browser.find_by_css(css_selector)

    def __init__(self, splinter_browser: DriverAPI = None, should_try_url_open=False):
        self.browser = splinter_browser or None  # or none because i think splinter implement singleton browser
        self.page_url = BASE_UI_TEST_URL + self.URL
        if should_try_url_open:
            self.browser.visit(self.page_url)
