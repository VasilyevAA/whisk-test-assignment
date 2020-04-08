import requests

STATUS_CODES = requests.codes


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
