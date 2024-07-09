import json


def read_json(filepath1, filepath2):
    with open(filepath1) as fh1:
        data1 = json.load(fh1)
    with open(filepath2) as fh2:
        data2 = json.load(fh2)
    return data1, data2
