import json


def format_json_lazy(data: dict) -> dict:
    def _inner(data: dict):
        new_d = {}
        for k, v in data.items():
            key, flag = k
            new_k = f"{key} [{flag}]"
            if isinstance(v, dict):
                new_v = _inner(v)
            else:
                new_v = v
            new_d[new_k] = new_v
        return new_d

    return _inner(data)


def format_json(data: dict) -> str:
    """ Represent diff between two files in json-format """
    data = format_json_lazy(data)
    return json.dumps(data)
