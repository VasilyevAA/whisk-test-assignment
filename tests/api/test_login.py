import pytest

from setting import WHISK_CLIENT_ID
from actions_api.whisk import get_unauthorized_client
from utils.common import STATUS_CODES, get_params_argv, Value
from utils.generate import generate_value

INVALID_TOKENS = get_params_argv({
    'token_is_empty': "",
    'token_is_not_exist': generate_value(64),
    'token_is_very_long': generate_value(10000),

})

INCORRECT_TOKENS = get_params_argv({
    'token_is_null': {"clientId": Value(None)},
    'without_token_field': {'data': {}}
})


class TestLogin:

    def setup(self):
        self.client = get_unauthorized_client()

    def test_positive_login_with_valid_credential(self):  # Could be use soft assert
        code, data = self.client.login_anonymous(WHISK_CLIENT_ID)
        assert code == STATUS_CODES.ok
        assert 'user' in data
        token_info = data.get('token')
        assert token_info
        assert token_info.get('access_token'), "Token is empty"
        assert token_info.get('token_type'), "Token type is empty"

    @pytest.mark.parametrize('client_id', **INVALID_TOKENS)
    def test_negative_login_with_invalid_token(self, client_id):
        code, data = self.client.login_anonymous(client_id)
        assert code == STATUS_CODES.bad
        assert data
        assert 'token' not in data

    @pytest.mark.parametrize('token_data', **INCORRECT_TOKENS)
    def test_negative_login_with_incorrect_token(self, token_data):
        code, data = self.client.login_anonymous(**token_data)
        assert code == STATUS_CODES.unauthorized
        assert data
        assert 'token' not in data

    def test_negative_login_with_not_exist_or_blocked_client_id(self):
        # it's expired or not verified token from https://developers.whisk.com/tools/create-account
        invalid_token = "hSugagKt8Tdk3Y1CtV8G6DEw977fZ17aCktZCSEBHfdSgCb6GQDMizScmUP5vno9"
        code, data = self.client.login_anonymous(invalid_token)
        assert code == STATUS_CODES.bad
        assert data
        assert 'token' not in data


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
