import allure

from actions_ui.page_objects.shipping_list_page import ShoppingListPage
from utils.generate import generate_value


def test_some_browser_stuff(browser):
    """Test using real browser."""
    main_page = ShoppingListPage(browser, True)
    with allure.step('Signup on shopping list page'):
        signup_form = main_page.get_signup_form()
        signup_form.fill_email_or_phone(generate_value(20, suffix='@gmail.com'))
        signup_form.click_continue()
        main_page.check_signup_form_hidden()

    print('qweqwe')


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
