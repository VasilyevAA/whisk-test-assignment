from splinter.driver.webdriver import WebDriverElement

from utils.client_qa_ui import PageObjectQA


class SignUpForm:

    def __init__(self, form_element: WebDriverElement):
        self.root_form = form_element

    def fill_email_or_phone(self, email_or_phone):
        input = self.root_form.find_by_css('[data-testid = "UI_KIT_INPUT"]')
        return input.fill(email_or_phone)

    def click_continue(self):
        self.root_form.find_by_css('[data-testid = "auth-continue-button"]').click()


class ShoppingListPage(PageObjectQA):
    URL = "/shopping-list"

    AUTH_FORM_CSS = '[data-testid = "authentication-form"]'

    def __init__(self, browser=None, open_page=False):
        super().__init__(browser, should_try_url_open=open_page)

    def get_signup_form(self):
        return SignUpForm(self.browser.find_by_css(self.AUTH_FORM_CSS))

    def check_signup_form_hidden(self):
        self.browser.is_element_not_present_by_css(self.AUTH_FORM_CSS)
