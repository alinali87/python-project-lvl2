from gendiff.json_helpers import read_json
from gendiff.yml_helpers import read_yml


def diff_data(data1: dict, data2: dict) -> dict:
    def _inner_keys_to_tuples(d):
        """ Convert all keys in a dictionary to (k, 0) tuples """
        if not isinstance(d, dict):
            return d
        new_d = {}
        for k, v in d.items():
            v = _inner_keys_to_tuples(v)
            new_d[(k, 0)] = v
        return new_d

    def _inner_diff(data1: dict, data2: dict, acc: dict = {}):
        """ Generate dictionary showing the difference between two data,
            (key, 0) -> no difference for this key
            (key, -1) -> key exists only in data1
            (key, 1) -> key exists only in data2

        Args:
            data1: data to compare
            data2: data to compare
            acc: accumulated difference between two data
        """
        all_keys = set(data1.keys()) | set(data2.keys())
        for key in all_keys:
            # only in data2
            if key not in data1.keys():
                acc[(key, 1)] = _inner_keys_to_tuples(data2[key])
            # only in data1
            elif key not in data2.keys():
                acc[(key, -1)] = _inner_keys_to_tuples(data1[key])
            # key in both and values are equal
            elif data1[key] == data2[key]:
                acc[(key, 0)] = _inner_keys_to_tuples(data1[key])
            # values are different
            elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
                acc[(key, 0)] = diff_data(data1[key], data2[key])
            else:
                acc[(key, -1)] = _inner_keys_to_tuples(data1[key])
                acc[(key, 1)] = _inner_keys_to_tuples(data2[key])
        return acc

    return _inner_diff(data1, data2)


def stylish(data, replacer: str = " ", count: int = 4) -> str:
    """ Produce formatted diff as a string

    Args:
        data: diff between two files to be formatted
        replacer: element to indent nested levels
        count: number of replacers for indentation
    Return:
        formatted difference between two files, e.g.
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
    def _inner(data, level: int = 1):
        if not isinstance(data, dict):
            if isinstance(data, bool):
                return 'true' if data else 'false'
            if data is None:
                return 'null'
            return str(data)
        formatted_list = ["{"]
        for k, v in sorted(data.items()):
            key, flag = k
            sign = {-1: "-", 0: " ", 1: "+"}[flag]
            value = _inner(v, level + 1)
            if value:
                formatted_list.append(replacer * (count * level - 2) + sign + " " + str(key) + ": " + value)
            else:
                formatted_list.append(replacer * (count * level - 2) + sign + " " + str(key) + ":")
        formatted_list.append(replacer * count * (level - 1) + "}")
        return "\n".join(formatted_list)

    return _inner(data)


def _stringify(value, replacer: str = " ", spaces_count: int = 1):
    def inner_stringify(value, level: int = 1):
        if not isinstance(value, dict):
            return str(value)
        pre = ["{"]
        for k, v in value.items():
            pre.append(replacer * spaces_count * level + str(k) + ": " + inner_stringify(v, level + 1))
        pre.append(replacer * spaces_count * (level - 1) + "}")
        return "\n".join(pre)

    return inner_stringify(value)


def generate_diff(filepath1: str, filepath2: str, format: str = "stylish") -> str:
    """ Generate difference between two json-files

    Args:
        filepath1: path to the first file
        filepath2: path to the second file
        format: name of formatter function to be used to produce the output
    Returns:
        str: difference between two files
    """
    diff = None
    if filepath1.endswith(".json") and filepath2.endswith(".json"):
        diff = diff_data(*read_json(filepath1, filepath2))

    if filepath1.endswith((".yml", ".yaml")) \
            and filepath2.endswith((".yml", ".yaml")):
        diff = diff_data(*read_yml(filepath1, filepath2))

    formatters = {
        "stylish": stylish,
    }
    if format not in formatters:
        raise NotImplementedError(f"Format {format} does not exist")
    format_function = formatters[format]
    return format_function(diff)
