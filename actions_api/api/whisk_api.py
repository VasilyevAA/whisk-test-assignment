from utils.client_qa_api import ClientApi


class WhiskApi:
    def __init__(self, whisk_client: ClientApi):
        self.client = whisk_client

    def login_anonymous(self, clientId=None, data=None):
        uri = '/auth/anonymous/create'
        data = data or {
            "clientId": clientId
        }
        return self.client.post(uri, body=data)

    def logout(self):
        raise NotImplementedError

    def create_shopping_list(self, name=None, language=None, recipes=None, rawItems=None, items=None):
        uri = '/v1/lists'
        data = {
            "name": name,
            "language": language,
            "recipes": recipes,
            "rawItems": rawItems,
            "items": items,
        }
        return self.client.post(uri, body=data)

    def add_item_to_shopping_list(self, shoping_list_id, name=None, language=None, recipes=None, rawItems=None, items=None):
        uri = f'/v1/{shoping_list_id}/items'
        data = {
            "name": name,
            "language": language,
            "recipes": recipes,
            "rawItems": rawItems,
            "items": items,
        }
        return self.client.post(uri, data=data)

    def delete_item_from_shopping_list(self):
        raise NotImplementedError

    def get_shopping_lists(self):
        uri = '/v1/lists'
        return self.client.get(uri)
