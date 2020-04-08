import pytest

from utils import run_test, checks
from utils.generate import generate_number
from utils.common import STATUS_CODES, get_params_argv
from actions_api.whisk import get_auth_client, generate_shopping_item, generate_shopping_list


ITEMS_FOR_PARAMETRIZE = get_params_argv({
    'zero_items': [],
    'without_items_field': None,
    'one_item': [generate_shopping_item()],
    'many_item': [generate_shopping_item() for i in range(generate_number(2, 4))],
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


if __name__ == '__main__':
    run_test(__file__)
