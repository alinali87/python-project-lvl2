def format_stylish(data, replacer: str = " ", count: int = 4) -> str:
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
            # TODO: clean up
            if key == "default":
                print("LEADE:", type(v), v, ord(v))

            sign = {-1: "-", 0: " ", 1: "+"}[flag]
            value = _inner(v, level + 1)
            hack = replacer * (count * level - 2) + sign + " " + str(key) + ": " + value
            formatted_list.append(hack.rstrip())
            # TODO: clean
            # if value:
            #     formatted_list.append(replacer * (count * level - 2) + sign + " " + str(key) + ": " + value)
            # else:
            #     formatted_list.append(replacer * (count * level - 2) + sign + " " + str(key) + ":")
        formatted_list.append(replacer * count * (level - 1) + "}")
        return "\n".join(formatted_list)

    return _inner(data)
