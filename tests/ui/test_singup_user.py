from actions_ui.common import PopupMsgTempaltes
from actions_ui.shopping_list import sign_up_user
from actions_ui.page_objects.shipping_list_page import ShoppingListPage


def test_signup_user(browser):
    shopping_list = ShoppingListPage(browser, True)
    username = sign_up_user(shopping_list)
    shopping_list.wait_popup_hidden(PopupMsgTempaltes.SIGN_UP)
    active_username = shopping_list.get_active_username()
    assert username == active_username


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
