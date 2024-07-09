from gendiff import generate_diff
import pytest
import json


test_cases = [("data/file1.json", "data/file2.json", "data/expected_diff.txt"),
              ("data/file1.yml", "data/file2.yml", "data/expected_diff.txt")]


@pytest.mark.parametrize("file1, file2, expected_file", test_cases)
def test_generate_diff(file1, file2, expected_file):
    output = generate_diff(file1, file2)
    with open(expected_file, "r") as fh:
        expected = fh.read()
    assert output == expected
