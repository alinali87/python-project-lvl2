import json
import yaml
import pytest
from gendiff import generate_diff, diff_data
from gendiff.formatters.format_stylish import format_stylish
from gendiff.formatters.format_plain import format_plain
from gendiff.formatters.format_json import format_json


test_cases = [("data/flat/file1.json", "data/flat/file2.json", "data/flat/expected_diff.txt"),
              ("data/flat/file1.yml", "data/flat/file2.yml", "data/flat/expected_diff.txt"),
              ("data/nested/file1.json", "data/nested/file2.json", "data/nested/expected_diff.txt")]


@pytest.mark.parametrize("file1, file2, expected_file", test_cases)
def test_generate_diff(file1, file2, expected_file):
    output = generate_diff(file1, file2)
    with open(expected_file, "r") as fh:
        expected = fh.read()
    assert output == expected


# diff data test cases
with open("data/nested/file1.json") as fh:
    data_json_1 = json.load(fh)
with open("data/nested/file2.json") as fh:
    data_json_2 = json.load(fh)
with open("data/nested/file1.yml") as fh:
    data_yaml_1 = yaml.safe_load(fh)
with open("data/nested/file2.yml") as fh:
    data_yaml_2 = yaml.safe_load(fh)


raw_diff = {
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
        },
        ("default", -1): None,
        ("default", 1): "",
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


@pytest.mark.parametrize("data1, data2, expected", [(data_json_1, data_json_2, raw_diff),
                                                    (data_yaml_1, data_yaml_2, raw_diff)])
def test_diff_data(data1, data2, expected):
    output = diff_data(data1, data2)
    assert output == expected


# format_stylish test cases
diff1 = {("a", 0): 1}
expected1 = "{\n  a: 1\n}"
diff2 = {("a", -1): {("aaa", 0): 123}, ("b", 1): True}
expected2 = "{\n  - a: {\n        aaa: 123\n    }\n  + b: true\n}"


@pytest.mark.parametrize("data, replacer, count, expected", [(diff1, " ", 2, expected1), (diff2, " ", 4, expected2)])
def test_format_stylish(data, replacer, count, expected):
    output = format_stylish(data, replacer, count)
    assert output == expected


# format_plain test cases
with open("data/nested/expected_plain_diff.txt") as fh:
    expected_plain_diff = fh.read()


@pytest.mark.parametrize("data, expected", [(raw_diff, expected_plain_diff)])
def test_format_plain(data, expected):
    output = format_plain(data)
    assert output == expected


# format_json test cases
expected_json_diff = json.dumps({
    "common [0]":
        {"follow [1]": False,
         "setting1 [0]": "Value 1",
         "setting2 [-1]": 200,
         "setting3 [-1]": True,
         "setting3 [1]": None,
         "setting4 [1]": "blah blah",
         "setting5 [1]": {"key5 [0]": "value5"},
         "setting6 [0]": {
             "doge [0]": {"wow [-1]": "", "wow [1]": "so much"},
             "key [0]": "value", "ops [1]": "vops"},
         "default [-1]": None,
         "default [1]": "",
         },
    "group1 [0]":
        {"baz [-1]": "bas",
         "baz [1]": "bars",
         "foo [0]": "bar",
         "nest [-1]":
             {"key [0]": "value"},
         "nest [1]": "str"
         },
    "group2 [-1]":
        {"abc [0]": 12345,
         "deep [0]": {"id [0]": 45}
         },
    "group3 [1]":
        {"deep [0]": {"id [0]": {"number [0]": 45}},
         "fee [0]": 100500
         }
})


@pytest.mark.parametrize("data, expected", [(raw_diff, expected_json_diff)])
def test_format_json(data, expected):
    output = format_json(data)
    assert output == expected
