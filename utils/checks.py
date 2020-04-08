from typing import List

import pytest
from datatest import validate, accepted, Extra


def eq_list(actual: List, expected: List, sorted_fn=None):
    """
    lists should be sorted

    This solution have many problem, but for good solution need use complex methods and libs
    for create common "validator" for different data structures
    """
    _sort_fn = lambda data: list(sorted(data, key=sorted_fn))
    actual, expected = _sort_fn(actual), _sort_fn(expected)
    assert len(actual) == len(expected), "Lists have different length"
    for i, ex_data in enumerate(expected):
        with accepted(Extra):
            validate(actual[i], ex_data, "")


class TestCheckAsserts:

    def test_positive_eq_list_required_have_missing(self):
        data = [{'id': 11, 'qwe': 12312}]

        requirement = [{'id': 11}]
        eq_list(data, requirement)

    def test_negative_eq_list_required_have_diff_value_in_required(self):
        data = [{'id': 11, 'qwe': 12312}]
        requirement = [{'id': 11, 'qwe': 333333}]
        with pytest.raises(AssertionError):
            eq_list(data, requirement)

    def test_negative_eq_list_diff_length(self):
        data = [{'id': 11, 'qwe': 12312}]
        requirement = [{'id': 11}, {'id': 22}]
        with pytest.raises(AssertionError):
            eq_list(data, requirement)


if __name__ == '__main__':
    from utils import run_test
    run_test(__file__)
