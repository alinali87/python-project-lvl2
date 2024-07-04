import json


def generate_diff(filepath1: str, filepath2: str) -> str:
    """ Generate difference between two json-files

    Args:
        filepath1: path to the first file
        filepath2: path to the second file
    Returns:
        str: difference between two files, e.g.
        {
          - follow: false
            host: hexlet.io
          - proxy: 123.234.53.22
          - timeout: 50
          + timeout: 20
          + verbose: true
        }
        where "-" means the key is missing in the 2d file,
                "+" means the key is missing in the 1st file,
                no sign means that both files have the same value
    """
    with open(filepath1) as fh1:
        data1 = json.load(fh1)
    with open(filepath2) as fh2:
        data2 = json.load(fh2)
    # ASSUME: all the keys are unique in a file
    all_keys = set(data1.keys()) | set(data2.keys())
    pre = []
    for key in all_keys:
        # only in data2
        if key not in data1.keys():
            pre.append((key, 1, data2[key], "+"))
        # only in data1
        elif key not in data2.keys():
            pre.append((key, -1, data1[key], "-"))
        # key in in both and values are equal
        elif data1[key] == data2[key]:
            pre.append((key, 0, data1[key], " "))
        # values are different
        else:
            pre.append((key, -1, data1[key], "-"))
            pre.append((key, 1, data2[key], "+"))
    pre.sort()
    formatted_list = ["{"]
    for key, int_sign, value, sign in pre:
        # TODO: got False instead of false.
        formatted_list.append(f"  {sign} {key}: {value}")
    formatted_list.append("}")
    return "\n".join(formatted_list)

