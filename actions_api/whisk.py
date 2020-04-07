
from utils.common import STATUS_CODES, ClientApi
from actions_api.api.whisk_api import WhiskApi
from setting import BASE_API_TEST_URL, WHISK_CLIENT_ID


def get_unauthorized_client():
    return WhiskApi(ClientApi(BASE_API_TEST_URL))


def get_auth_client():
    code, data = WhiskApi(ClientApi(BASE_API_TEST_URL)).login_anonymous(WHISK_CLIENT_ID)
    assert code == STATUS_CODES.ok, str(data)
    token_info = data['token']
    auth_header = {"Authorization": f"{token_info['token_type']} {token_info['access_token']}"}
    return WhiskApi(ClientApi(BASE_API_TEST_URL, additional_headers=auth_header))


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
