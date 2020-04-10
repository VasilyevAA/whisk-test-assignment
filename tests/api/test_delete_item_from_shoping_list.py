from utils.checks import eq_list
from utils.common import STATUS_CODES
from actions_api.whisk import generate_shopping_item, generate_shopping_list, get_auth_client, MAX_ITEM_IN_LIST, \
    MSG_MAX_ITEM_DESCRIPTION_ERROR


class TestDeleteItemFromShoppingList:

    def setup(self):
        self.client = get_auth_client()

    def prepare_shopping_list(self, count_of_product=2):
        items = [generate_shopping_item() for i in range(count_of_product)]
        shopping_list = generate_shopping_list(items=items)
        code, sl_data = self.client.create_shopping_list(**shopping_list)
        assert code == STATUS_CODES.ok
        return sl_data['id'], sl_data['items']

    def test_positive_delete_item_from_shopping_list(self):
        shopping_list_id, items = self.prepare_shopping_list()
        code, add_item_data = self.client.add_item_to_shopping_list(
            shopping_list_id, items=[{'id': items[0]['id'], 'deleted': True}]
        )
        assert code == STATUS_CODES.ok
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(items) - 1 == data[0]['itemsCount']
        
    def test_negative_delete_items_more_than_max(self):
        shopping_list_id, items = self.prepare_shopping_list(MAX_ITEM_IN_LIST)
        additional_items = [generate_shopping_item()]
        code, add_item_data = self.client.add_item_to_shopping_list(shopping_list_id, items=additional_items)
        assert code == STATUS_CODES.ok
        expected_items = items + add_item_data['items']
        code, add_item_data = self.client.add_item_to_shopping_list(
            shopping_list_id, items=[{'id': it['id'], 'deleted': True} for it in expected_items]
        )
        assert code == STATUS_CODES.bad
        assert add_item_data['code']
        assert MSG_MAX_ITEM_DESCRIPTION_ERROR in add_item_data['code']
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(expected_items) == data[0]['itemsCount']

    def test_negative_delete_items_twice_from_shopping_list_from__two_response(self):
        shopping_list_id, items = self.prepare_shopping_list()
        delete_items = [{'id': items[0]['id'], 'deleted': True}]
        for i in range(2):
            code, add_item_data = self.client.add_item_to_shopping_list(shopping_list_id, items=delete_items)
            assert code == STATUS_CODES.ok
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(items) - 1 == data[0]['itemsCount']

    def test_negative_delete_items_twice_from_shopping_list_from_one_response(self):
        shopping_list_id, items = self.prepare_shopping_list()
        delete_items = [{'id': items[0]['id'], 'deleted': True}] * 2
        code, add_item_data = self.client.add_item_to_shopping_list(shopping_list_id, items=delete_items)
        assert code == STATUS_CODES.bad
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(items) == data[0]['itemsCount']

    def test_negative_delete_items_exist_item_from_another_shopping_list(self):
        another_shopping_list_id, items = self.prepare_shopping_list()
        shopping_list_id, items_actual = self.prepare_shopping_list()
        delete_items = [{'id': items[0]['id'], 'deleted': True}]
        code, add_item_data = self.client.add_item_to_shopping_list(shopping_list_id, items=delete_items)
        assert code == STATUS_CODES.ok
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        actual_shopping_lists = [{'id': i['id'], 'itemsCount': i['itemsCount']} for i in data]
        expected_data = [
            {'id': another_shopping_list_id, 'itemsCount': len(items)},
            {'id': shopping_list_id, 'itemsCount': len(items_actual)}
        ]
        eq_list(actual_shopping_lists, expected_data, lambda data: data['id'])


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
