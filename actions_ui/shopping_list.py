import allure

from utils.generate import generate_value


def sign_up_user(shopping_list_page, username=None):
    username = username or generate_value(20, suffix='@gmail.com')
    with allure.step('Signup on shopping list page'):
        signup_form = shopping_list_page.get_signup_form()
        signup_form.fill_email_or_phone(username)
        signup_form.click_continue()
        shopping_list_page.check_signup_form_hidden()
        return username


def add_item_in_shopping_list(shopping_list_page, search_name='', item_name=None):
    shopping_list_page.add_item_to_list(search_name)
    shopping_list_page.wait_items_dropdown()
    added_item_name = shopping_list_page.click_on_dropdown_item_with_name(item_name)
    return added_item_name

