from utils.generate import generate_number
from actions_ui.common import PopupMsgTempaltes
from actions_ui.page_objects.shipping_list_page import ShoppingListPage
from actions_ui.shopping_list import add_item_in_shopping_list, sign_up_user


def test_add_items_in_shopping_list(func_browser):
    shopping_list = ShoppingListPage(func_browser, True)
    sign_up_user(shopping_list)
    expected_items = []
    add_items = ['Milk 1%', 'Milk chocolate']
    for add_item in add_items:
        expected_items.append(add_item_in_shopping_list(shopping_list, 'Milk', add_item))

    delete_item_name = add_items.pop(generate_number(0, len(add_items) - 1))
    item_form = shopping_list.open_item_detail(delete_item_name)
    item_form.delete_item()
    shopping_list.wait_popup_hidden(PopupMsgTempaltes.DELETE_ITEM % delete_item_name)
    items_in_shopping_list = shopping_list.get_added_items_in_shopping_list()
    assert set(add_items) == {i.text for i in items_in_shopping_list}


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
