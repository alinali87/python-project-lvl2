import yaml


def read_yml(filepath1, filepath2):
    with open(filepath1) as fh1:
        data1 = yaml.safe_load(fh1)
    with open(filepath2) as fh2:
        data2 = yaml.safe_load(fh2)
    return data1, data2
