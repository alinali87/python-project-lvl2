from gendiff import generate_diff, diff_data, stylish
import pytest
import json


test_cases = [("data/flat/file1.json", "data/flat/file2.json", "data/flat/expected_diff.txt"),
              ("data/flat/file1.yml", "data/flat/file2.yml", "data/flat/expected_diff.txt"),
              ("data/nested/file1.json", "data/nested/file2.json", "data/nested/expected_diff.txt")]


@pytest.mark.parametrize("file1, file2, expected_file", test_cases)
def test_generate_diff(file1, file2, expected_file):
    output = generate_diff(file1, file2)
    with open(expected_file, "r") as fh:
        expected = fh.read()
    assert output == expected


# TODO: use fixtures
# TODO: document:
# -1: add a "-" sign, i.e. present only in 1st
# 1: add a "+" sign, i.e. present only in 2d
# 0: add " " sign, but this can mean two things: either present in both, or a key in a nested structure that does not have to be parsed (nested structue is present only in one file)
with open("data/nested/file1.json") as fh:
    data1 = json.load(fh)
with open("data/nested/file2.json") as fh:
    data2 = json.load(fh)
expected_diff = {
    ("common", 0): {
        ("follow", 1): False,
        ("setting1", 0): "Value 1",
        ("setting2", -1): 200,
        ("setting3", -1): True,
        ("setting3", 1): None,
        ("setting4", 1): "blah blah",
        ("setting5", 1): {
         ("key5", 0): "value5",
        },
        ("setting6", 0): {
         ("doge", 0): {
             ("wow", -1): "",
             ("wow", 1): "so much",
         },
         ("key", 0): "value",
         ("ops", 1): "vops",
        }
    },
    ("group1", 0): {
        ("baz", -1): "bas",
        ("baz", 1): "bars",
        ("foo", 0): "bar",
        ("nest", -1): {
            ("key", 0): "value"
        },
        ("nest", 1): "str",
    },
    ("group2", -1): {
        ("abc", 0): 12345,
        ("deep", 0): {
            ("id", 0): 45,
        }
    },
    ("group3", 1): {
        ("deep", 0): {
            ("id", 0): {
                ("number", 0): 45,
            }

        },
        ("fee", 0): 100500,
    }
}


@pytest.mark.parametrize("data1, data2, expected", [(data1, data2, expected_diff)])
def test_diff_data(data1, data2, expected):
    output = diff_data(data1, data2)
    assert output == expected


# TODO: move tests to fixtures
diff1 = {("a", 0): 1}
expected1 = "{\n  a: 1\n}"
diff2 = {("a", -1): {("aaa", 0): 123}, ("b", 1): True}
expected2 = "{\n  - a: {\n        aaa: 123\n    }\n  + b: true\n}"


@pytest.mark.parametrize("data, replacer, count, expected", [(diff1, " ", 2, expected1), (diff2, " ", 4, expected2)])
def test_stylish(data, replacer, count, expected):
    output = stylish(data, replacer, count)
    assert output == expected


# TODO: clean up
def test_temporary():
    def _inner_keys_to_tuples(d):
        """ Convert all keys in a dictionary to (k, 0) tuples """
        if not isinstance(d, dict):
            return d
        new_d = {}
        for k, v in d.items():
            v = _inner_keys_to_tuples(v)
            new_d[(k, 0)] = v
        return new_d

    d = {"a": 1}
    assert _inner_keys_to_tuples(d) == {("a", 0): 1}
    d2 = {"a": {"b": {1: 12345}}}
    assert _inner_keys_to_tuples(d2) == {("a", 0): {("b", 0): {(1, 0): 12345}}}
