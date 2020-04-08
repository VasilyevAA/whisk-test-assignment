from utils import run_test
from utils.common import STATUS_CODES
from utils.generate import generate_number
from actions_api.whisk import get_auth_client, generate_shopping_item, generate_shopping_list


class TestGetShoppingList:

    def setup(self):
        self.client = get_auth_client()

    def test_positive_get_shopping_list(self):
        items = [generate_shopping_item() for i in range(generate_number(0, 1))]
        shopping_list = generate_shopping_list(items=items)
        code, sl_data = self.client.create_shopping_list(**shopping_list)
        assert code == STATUS_CODES.ok
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert len(data) == 1
        shopping_list = data[0]
        assert shopping_list['id'] == sl_data['id']
        assert shopping_list['itemsCount'] == len(items)

    def test_negative_get_shopping_list_without_created_shopping_list(self):
        code, data = self.client.get_shopping_lists()
        assert code == STATUS_CODES.ok
        assert not data


if __name__ == '__main__':
    run_test(__file__)
