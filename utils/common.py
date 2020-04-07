import json
from contextlib import contextmanager
from pprint import pprint

import allure
import requests
from loguru import logger


STATUS_CODES = requests.codes


class Methods:
    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


class Value(object):
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


def filter_dict_from_none(dict_to_filter):
    return {
        key: value if not isinstance(value, Value) else value.value
        for key, value in dict_to_filter.items() if value is not None
    }


def get_params_argv(params):
    return {
        'argvalues': list(params.values()),
        'ids': list(params.keys())
    }


class ApiLogger:

    def __init__(self, logger_name):
        self._messages = []
        self.api_logger = logger.bind(name=logger_name)

    def msg(self, *messages):
        message = ' '.join([str(message) for message in messages])
        self._messages.append(message)
        self.api_logger.info(message)

    def get_all_msg(self):
        return '\n'.join(self._messages)

    def clear_buffer(self):
        self._messages = []

    @contextmanager
    def buffer_messages(self, attach_name):
        self.clear_buffer()
        yield self
        allure.attach(attach_name)
        self.clear_buffer()


class ClientApi:

    def __init__(self, base_url, service_name=None, additional_headers=None):
        self.service_link = base_url
        self.service_name = service_name or base_url
        self.headers = dict({
            'Content-Type': 'application/json',
        }, **(additional_headers or {}))
        self.api_logger = ApiLogger(self.service_name)
        self._cookies = {}
        self._session = requests.Session()

    def _format_res(self, resp, resp_text):
        return resp.status_code, resp_text

    def _format_uri_value_fn(self, data):
        return ','.join(str(i) for i in data) if isinstance(data, (list, set)) else data

    def _get_target_uri(self, uri, query_params):
        if query_params:
            query_params = filter_dict_from_none(query_params)
            query_uri = "&".join(["%s=%s" % (k, self._format_uri_value_fn(v)) for k, v in query_params.items()])
            if query_uri:
                query_uri = "?" + query_uri
            return self.service_link + uri + query_uri
        return self.service_link + uri

    def _format_body(self, body):
        if isinstance(body, dict):
            data = filter_dict_from_none(body)
        else:
            data = body
        return data

    def _request(self, type_request, uri, data, headers=None, verify=True, **request_params):
        self._messages = []
        if type_request not in (Methods.GET, Methods.POST, Methods.PUT, Methods.PATCH, Methods.DELETE):
            raise Exception("Unknown request type: %s" % type_request)
        headers = filter_dict_from_none(dict(self.headers, **(headers or {})))
        request_params = dict({
            'headers': headers,
            'verify': verify,
        }, **request_params)
        if type_request != Methods.GET:
            data = json.dumps(data)
            request_params.update({'data': data})
        with self.api_logger.buffer_messages('Request info'):
            with allure.step(f"Step: {type_request} to the service: {uri}"):
                method_request = getattr(self._session, type_request.lower())
                self.api_logger.msg("Step: %s to the service: %s" % (type_request, uri))
                self.api_logger.msg("headers of request:", headers)
                self.api_logger.msg("body of request:", data)
                resp = method_request(uri, **request_params)
                self.api_logger.msg("Service code: %s" % resp.status_code)
                try:
                    json_resp = resp.json()
                    res = self._format_res(resp, json_resp)
                except ValueError:
                    res = self._format_res(resp, resp.text)
                _, response = res
                self.api_logger.msg("Response:", response)
                return res

    def post(self, uri, body=None, query_params=None, headers=None, **kwargs):
        uri = self._get_target_uri(uri, query_params)
        data = self._format_body(body)
        return self._request(Methods.POST, uri, data, headers, **kwargs)

    def get(self, uri, body=None, query_params=None, headers=None):
        uri = self._get_target_uri(uri, query_params)
        return self._request(Methods.GET, uri, "", headers)
