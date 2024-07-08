from gendiff import generate_diff
import pytest
import json


@pytest.mark.parametrize("file1, file2, expected_file", [("data/file1.json", "data/file2.json", "data/expected1.txt")])
def test_generate_diff(file1, file2, expected_file):
    output = generate_diff(file1, file2)
    with open(expected_file, "r") as fh:
        expected = fh.read()
    assert output == expected
