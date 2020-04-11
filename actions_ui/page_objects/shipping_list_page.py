from utils.client_qa_ui import PageObjectQA, WebElementObjQA


class SignUpForm(WebElementObjQA):

    def fill_email_or_phone(self, email_or_phone):
        input = self.find_by_testid("UI_KIT_INPUT")
        return input.fill(email_or_phone)

    def click_continue(self):
        self.find_by_testid("auth-continue-button").click()


class ItemForm(WebElementObjQA):

    def delete_item(self):
        button = self.find_by_testid("edit-item-delete-button", 'button')
        button.click()


class ShoppingListPage(PageObjectQA):
    URL = "/shopping-list"

    AUTH_FORM_TESTID = "authentication-form"
    AUTOCOMPLETE_ITEM_TESTID = "desktop-add-item-autocomplete"

    def __init__(self, browser=None, open_page=False):
        super().__init__(browser, should_try_url_open=open_page)

    def get_active_username(self):
        elem = self.find_by_testid("avatar-button", "", ">div:nth-child(2)")
        return elem.text

    def get_signup_form(self):
        return SignUpForm(self.find_by_testid(self.AUTH_FORM_TESTID))

    def check_signup_form_hidden(self):
        assert self.browser.is_element_present_by_css(self.TESTID_CSS_TEMPLATE % self.AUTH_FORM_TESTID)
        assert self.browser.is_element_not_present_by_css(self.TESTID_CSS_TEMPLATE % self.AUTH_FORM_TESTID)

    def add_item_to_list(self, item_name):
        elem = self.find_by_testid(self.AUTOCOMPLETE_ITEM_TESTID, "input")
        elem.fill(item_name)

    def wait_items_dropdown(self):
        assert self.browser.is_element_present_by_css('div' + self.TESTID_CSS_TEMPLATE % self.AUTOCOMPLETE_ITEM_TESTID)

    def click_on_dropdown_item_with_name(self, name=None):
        elems = self.find_by_testid(self.AUTOCOMPLETE_ITEM_TESTID, 'div', '>div>div ')
        if name is None:
            name = elems.text
            elems.click()
            return name
        for el in elems:
            if name.lower() == el.text.lower():
                name = el.text
                el.click()
                return name
        else:
            raise Exception(f"Can't find item with name '{name}'")

    def get_added_items_in_shopping_list(self):
        elems = self.find_by_testid("shopping-list-item-name")
        return elems

    def _get_item_detail_form(self):
        assert self.browser.is_element_present_by_css("form")
        return ItemForm(self.browser.find_by_css("form"))

    def open_item_detail(self, item_name):
        items = self.get_added_items_in_shopping_list()
        item = [i for i in items if i.text.lower() == item_name.lower()]
        assert len(item) == 1
        item = item[0]
        item.click()
        return self._get_item_detail_form()


