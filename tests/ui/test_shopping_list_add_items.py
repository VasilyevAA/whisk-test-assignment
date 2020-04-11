from actions_ui.page_objects.shipping_list_page import ShoppingListPage
from actions_ui.shopping_list import add_item_in_shopping_list, sign_up_user


def test_add_items_in_shopping_list(func_browser):
    shopping_list = ShoppingListPage(func_browser, True)
    sign_up_user(shopping_list)
    expected_items = []
    for add_item in ['Milk 1%', 'Milk chocolate']:
        expected_items.append(add_item_in_shopping_list(shopping_list, 'Milk', add_item))
    all_items = shopping_list.get_added_items_in_shopping_list()
    assert set(expected_items) == set(i.text for i in all_items)


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
