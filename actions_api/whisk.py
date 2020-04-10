import random

from utils.common import STATUS_CODES, filter_dict_from_none
from utils.client_qa_api import ClientApi
from actions_api.api.whisk_api import WhiskApi
from setting import BASE_API_TEST_URL, WHISK_CLIENT_ID
from utils.generate import generate_value, get_rnd_bool, generate_number

MIN_ITEM_IN_LIST = 0
MAX_ITEM_IN_LIST = 100


def get_unauthorized_client(headers=None):
    return WhiskApi(ClientApi(BASE_API_TEST_URL, additional_headers=headers))


def get_auth_client():
    code, data = get_unauthorized_client().login_anonymous(WHISK_CLIENT_ID)
    assert code == STATUS_CODES.ok, str(data)
    token_info = data['token']
    auth_header = {"Authorization": f"{token_info['token_type']} {token_info['access_token']}"}
    return get_unauthorized_client(auth_header)


def generate_shopping_item(name=None, **kwargs):
    data = {
        "name": name or generate_value()
    }
    if get_rnd_bool():
        data['quantity'] = generate_number(is_float=get_rnd_bool())
        data['unit'] = random.choice(['gram', 'ml'])
        data['comment'] = generate_value()
    if kwargs:
        data.update(**kwargs)
    return data


def generate_shopping_list(**kwargs):
    data = {
        'name': random.choice([None, generate_value()]),
        'items': random.choice([None, [generate_shopping_item() for i in range(generate_number(1, 2))]]),
    }
    if kwargs:
        data.update(**kwargs)
    return filter_dict_from_none(data)


if __name__ == '__main__':
    import requests
    import json
    client = get_auth_client()
    keks = {
          "name": "My Shopping List",
          "items": [
            {
              "quantity": 200,
              "unit": "g",
              "name": "smoked salmon"
            },
            {
              "quantity": 2,
              "unit": "slices",
              "name": "cheddar cheese",
              "comment": "extra mature"
            }
          ]
        }
    resp = requests.post('https://graph-dev.whisk.com/v1/lists', json.dumps(keks), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer 6mpRYDLGUSEPfDda8OJCS2dCuPF7HZwWTnGdWxJcYH8K3cCj1sxVZVMjGHx2FrD0'})
    code, data = client.create_shopping_list(**keks)
    client.get_shopping_lists()
