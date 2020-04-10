import pytest

from utils import run_test, checks
from utils.common import STATUS_CODES, get_params_argv
from actions_api.whisk import get_auth_client, generate_shopping_item, generate_shopping_list, MAX_ITEM_IN_LIST, \
    MSG_MAX_ITEM_DESCRIPTION_ERROR

ITEMS_FOR_PARAMETRIZE = get_params_argv({
    'zero_items': [],
    'without_items_field': None,
    'one_item': [generate_shopping_item()],
    'max_item': [generate_shopping_item() for i in range(MAX_ITEM_IN_LIST)],
})


class TestCreateShoppingList:

    def setup(self):
        self.client = get_auth_client()

    @pytest.mark.parametrize('shopping_items', **ITEMS_FOR_PARAMETRIZE)
    def test_positive_create_shopping_list(self, shopping_items):
        shopping_list = generate_shopping_list(items=shopping_items)
        code, data = self.client.create_shopping_list(**shopping_list)
        assert code == STATUS_CODES.ok
        sort_fn = lambda it: tuple(it.get(key) for key in ['name', 'quantity', 'comment'])
        checks.eq_list(data.get('items', []), shopping_items or [], sorted_fn=sort_fn)
        assert data.get('id')
        assert data.get('name') == shopping_list.get('name')
        assert data.get('language') == shopping_list.get('language', 'en')

    def test_negative_create_shopping_list_with_max_items(self):
        shopping_list = generate_shopping_list(items=[generate_shopping_item() for i in range(101)])
        code, data = self.client.create_shopping_list(**shopping_list)
        assert code == STATUS_CODES.bad
        assert data['code']
        assert MSG_MAX_ITEM_DESCRIPTION_ERROR in data['description']

    def test_negative_create_shopping_list_with_invalid_data(self):
        pytest.skip("NotImplementedError")

    def test_negative_create_shopping_list_without_auth(self):
        pytest.skip("NotImplementedError")


if __name__ == '__main__':
    run_test(__file__)
