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


class TestAddItemInShoppingList:

    def setup(self):
        self.client = get_auth_client()

    @pytest.mark.parametrize('additional_items', **ITEMS_FOR_PARAMETRIZE)
    def test_positive_add_item_in_shopping_list(self, additional_items):
        shopping_list = generate_shopping_list(items=[generate_shopping_item() for i in range(generate_number(max=3))])
        code, data = self.client.create_shopping_list(**shopping_list)
        shopping_list_id = data['id']
        assert code == STATUS_CODES.ok
        code, add_item_data = self.client.add_item_to_shopping_list(shopping_list_id, items=additional_items)
        assert code == STATUS_CODES.ok
        sort_fn = lambda it: tuple(it.get(key) for key in ['name', 'quantity', 'comment'])
        checks.eq_list(add_item_data.get('items', []), additional_items or [], sorted_fn=sort_fn)
        assert not add_item_data['combinedItems']
        assert not add_item_data['recipes']
        code, sl_data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(sl_data) == 1
        interested_shopping_list = sl_data[0]
        assert interested_shopping_list['id'] == shopping_list_id
        expected_items = shopping_list['items'] or [] + additional_items or []
        assert interested_shopping_list['itemsCount'] == len(expected_items)


if __name__ == '__main__':
    run_test(__file__)
