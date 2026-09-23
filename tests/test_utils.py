import json

from utils import invert_dictionary


def test_invert_dictionary_happy_path() -> None:
    input = {
        "1": ["apple", "banana", "carrot"],
        "2": ["apple", "banana"],
        "3": ["apple"],
    }

    actual = invert_dictionary(input)
    expected = {
        "apple": ["1", "2", "3"],
        "banana": ["1", "2"],
        "carrot": ["1"],
    }

    actual_json = json.dumps(actual)
    expected_json = json.dumps(expected)

    assert actual == expected
    assert actual_json == expected_json


def test_invert_empty_dictionary() -> None:
    input: dict = {}

    actual = invert_dictionary(input)
    expected: dict = {}

    actual_json = json.dumps(actual)
    expected_json = json.dumps(expected)

    assert actual == expected
    assert actual_json == expected_json


def test_invert_empty_list_is_lost() -> None:
    input: dict[str, list] = {"apple": []}

    actual = invert_dictionary(input)
    expected: dict = {}

    actual_json = json.dumps(actual)
    expected_json = json.dumps(expected)

    assert actual == expected
    assert actual_json == expected_json
